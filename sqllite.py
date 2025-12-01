import sqlite3
import numpy as np
from numpy.linalg import norm


# -----------------------------------
# Helper: Cosine similarity
# -----------------------------------
def cosine_similarity(v1, v2):
    v1 = np.frombuffer(v1, dtype=np.float32)
    v2 = np.frombuffer(v2, dtype=np.float32)
    return np.dot(v1, v2) / (norm(v1) * norm(v2) + 1e-10)


# -----------------------------------
# Create in-memory SQLite + table
# -----------------------------------
conn = sqlite3.connect(":memory:")

conn.execute("""
CREATE TABLE books_vectors (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    embedding BLOB NOT NULL
);
""")


# -----------------------------------
# Fake embeddings
# -----------------------------------
def make_vec(value: float) -> bytes:
    return np.array([value] * 384, dtype=np.float32).tobytes()


book_data = [
    (1, "Book 1: Intro to AI", make_vec(0.10)),
    (2, "Book 2: Cooking with Love", make_vec(0.80)),
    (3, "Book 3: Machine Learning", make_vec(0.14)),
]

conn.executemany("INSERT INTO books_vectors (id, title, embedding) VALUES (?, ?, ?)", book_data)
conn.commit()


# -----------------------------------
# Fake query embedding generator
# -----------------------------------
def fake_text_embedding(text: str) -> bytes:
    return np.array([0.15] * 384, dtype=np.float32).tobytes()


# -----------------------------------
# Query
# -----------------------------------
query_text = input("Enter your search text: ")
query_emb = fake_text_embedding(query_text)

cursor = conn.execute("SELECT id, title, embedding FROM books_vectors")
rows = cursor.fetchall()

# -----------------------------------
# Compute similarity manually
# -----------------------------------
scores = []
for row in rows:
    book_id, title, emb = row
    sim = cosine_similarity(query_emb, emb)
    scores.append((book_id, title, float(sim)))

# Sort descending by similarity
scores.sort(key=lambda x: x[2], reverse=True)

# Top-2 results
print("\nTop-2 similar books:")
for book_id, title, sim in scores[:2]:
    print(f"ID: {book_id} | Title: {title} | Similarity: {sim:.4f}")