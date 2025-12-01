import os
import json
import textwrap
import streamlit as st
from transformers import pipeline
import chromadb
from chromadb.utils import embedding_functions

# ---------------------------
# Config
# ---------------------------
st.set_page_config(page_title="Institute JSON RAG", page_icon="🏫", layout="wide")
st.title("🏫 Institute JSON RAG Chatbot (Per-item chunks, better embeddings)")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "institute_json_collection"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)

# ---------------------------
# Helpers: load JSON files
# ---------------------------
def load_json_files(data_dir):
    files = {}
    for fname in sorted(os.listdir(data_dir)):
        if fname.lower().endswith(".json"):
            try:
                with open(os.path.join(data_dir, fname), "r", encoding="utf-8") as f:
                    files[fname] = json.load(f)
            except Exception as e:
                st.error(f"Error reading {fname}: {e}")
    return files

# ---------------------------
# Helpers: convert course/student/institute info -> readable text
# ---------------------------
def course_to_text(course):
    parts = [
        f"Course Name: {course.get('name','')}",
        f"Course Code: {course.get('code','')}",
        f"Duration: {course.get('duration','')}",
        f"Semesters: {course.get('semesters','')}",
        f"Eligibility: {course.get('eligibility','')}",
        f"Fees: {course.get('fees','')}",
        f"Total Seats: {course.get('total_seats','')}",
    ]
    return "\n".join([p for p in parts if p])

def student_to_text(student):
    parts = [
        f"Name: {student.get('name','')}",
        f"Enrollment No: {student.get('enrollment_no','')}",
        f"Course: {student.get('course','')}",
        f"Year: {student.get('year','')}",
        f"Contact: {student.get('contact','')}",
        f"Fees Paid: {student.get('fees_paid','')}",
        f"Fees Pending: {student.get('fees_pending','')}",
    ]
    return "\n".join([p for p in parts if p])

def generic_item_to_text(item):
    if isinstance(item, dict):
        lines = []
        for k, v in item.items():
            if isinstance(v, (list, dict)):
                lines.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
            else:
                lines.append(f"{k}: {v}")
        return "\n".join(lines)
    else:
        return str(item)

# ---------------------------
# Build or get Chroma Collection
# ---------------------------
@st.cache_resource
def get_chroma_collection():
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    try:
        collection = client.get_collection(name=COLLECTION_NAME)
    except Exception:
        collection = client.create_collection(name=COLLECTION_NAME, embedding_function=ef)

    if collection.count() == 0:
        json_files = load_json_files(DATA_DIR)
        docs, metas, ids = [], [], []
        for fname, data in json_files.items():
            base = os.path.splitext(fname)[0]

            # Courses
            if isinstance(data, dict) and "courses" in data:
                for i, c in enumerate(data["courses"]):
                    text = course_to_text(c)
                    docs.append(text)
                    metas.append({"source": fname, "type":"course", "item_index":i})
                    ids.append(f"{base}-course-{i}")

            # Students
            if isinstance(data, dict) and "students" in data:
                for i, s in enumerate(data["students"]):
                    text = student_to_text(s)
                    docs.append(text)
                    metas.append({"source": fname, "type":"student", "item_index":i})
                    ids.append(f"{base}-student-{i}")

            # Fallback: everything else
            for k,v in data.items():
                if k not in ["courses","students"]:
                    text = generic_item_to_text({k:v})
                    docs.append(text)
                    metas.append({"source": fname, "type":"key_block", "key":k})
                    ids.append(f"{base}-key-{k}")

        # Chunk very long docs
        final_docs, final_metas, final_ids = [], [], []
        for doc, meta, id_ in zip(docs, metas, ids):
            if len(doc) > 1500:
                parts = textwrap.wrap(doc, width=800)
                for j, p in enumerate(parts):
                    final_docs.append(p)
                    nm = meta.copy()
                    nm["subchunk"] = j
                    final_metas.append(nm)
                    final_ids.append(f"{id_}-part-{j}")
            else:
                final_docs.append(doc)
                final_metas.append(meta)
                final_ids.append(id_)
        collection.add(documents=final_docs, metadatas=final_metas, ids=final_ids)

    return collection

# ---------------------------
# Load generator (FLAN-T5-Small)
# ---------------------------
@st.cache_resource
def load_generator():
    try:
        gen = pipeline("text2text-generation", model="google/flan-t5-small", device=-1)
        return gen
    except Exception as e:
        st.error(f"Could not load text generation model: {e}")
        return None

# ---------------------------
# Retrieval + prompt
# ---------------------------
def retrieve_context(query, top_k=3):
    collection = get_chroma_collection()
    res = collection.query(query_texts=[query], n_results=top_k)
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    return list(zip(docs, metas))

def build_prompt(history, user_q, context):
    lines = [
        "You are an Institute QA Assistant. Answer ONLY using the context below.",
        "If the answer cannot be found in the provided context, reply exactly: \"I don't know from this text.\"",
        "",
        "CONTEXT:"
    ]
    for i, (doc, meta) in enumerate(context, start=1):
        lines.append(f"[Chunk {i}] (Source: {meta.get('source')}, type: {meta.get('type')}, index: {meta.get('item_index')})")
        lines.append(doc)
        lines.append("")

    lines.append("CONVERSATION:")
    for msg in history:
        role = "User" if msg["role"] == "user" else "Bot"
        lines.append(f"{role}: {msg['text']}")
    lines.append(f"User: {user_q}")
    lines.append("Bot:")
    return "\n".join(lines)

# ---------------------------
# Chat UI
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"bot","text":"Hi! Ask about courses, students, fees, or placements."}]
if "last_context" not in st.session_state:
    st.session_state.last_context = []

st.sidebar.header("Settings")
if st.sidebar.button("Clear chat"):
    st.session_state.messages = [{"role":"bot","text":"Chat cleared."}]
    st.session_state.last_context = []

# show messages
for m in st.session_state.messages:
    if m["role"] == "user":
        st.markdown(f"**You:** {m['text']}")
    else:
        st.markdown(f"**Bot:** {m['text']}")

# input
user_q = st.text_input("Ask a question about the institute data:")
send_clicked = st.button("Send")

if send_clicked and user_q.strip():
    q = user_q.strip()
    with st.spinner("Retrieving relevant JSON chunks..."):
        ctx = retrieve_context(q, top_k=6)

    gen = load_generator()
    history = st.session_state.messages.copy()
    prompt = build_prompt(history, q, ctx)

    with st.spinner("Generating answer..."):
        if gen:
            out = gen(prompt, max_length=250)
            answer = out[0]["generated_text"].strip()
            if not answer:
                answer = "I don't know from this text."
        else:
            answer = "Model not available."

    st.session_state.messages.append({"role":"user","text":q})
    st.session_state.messages.append({"role":"bot","text":answer})
    st.session_state.last_context = ctx

# show context used
if st.session_state.last_context:
    with st.expander("📚 Context used (top chunks)"):
        for i, (doc, meta) in enumerate(st.session_state.last_context, start=1):
            st.markdown(f"**Chunk {i} — {meta.get('source')} — {meta.get('type')} — index:{meta.get('item_index')}**")
            st.write(doc)
