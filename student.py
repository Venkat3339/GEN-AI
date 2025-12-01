import sqlite3
import sqlite_vec
from sentence_transformers import SentenceTransformer

# 1️⃣ Setup
conn = sqlite3.connect("semantic.db")
conn.enable_load_extension(True)
sqlite_vec.load(conn)

conn.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT,
    embedding BLOB
);
""")

# 2️⃣ Model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 3️⃣ Insert data
data = [
    ("student_info", """Alexandra Thompson, a 19-year-old computer science sophomore with a 3.7 GPA,
    is a member of the programming and chess clubs who enjoys pizza, swimming, and hiking
    in her free time in hopes of working at a tech company after graduating from the University of Washington."""),
    
    ("club_info", """The university chess club provides an outlet for students to come together and enjoy playing
    the classic strategy game of chess. Members of all skill levels are welcome, from beginners learning
    the rules to experienced tournament players. The club typically meets a few times per week to play casual games,
    participate in tournaments, analyze famous chess matches, and improve members' skills."""),
    
    ("university_info", """The University of Washington, founded in 1861 in Seattle, is a public research university
    with over 45,000 students across three campuses in Seattle, Tacoma, and Bothell.
    As the flagship institution of the six public universities in Washington state,
    UW encompasses over 500 buildings and 20 million square feet of space,
    including one of the largest library systems in the world.""")
]

for title, text in data:
    embedding = model.encode(text)
    conn.execute("INSERT INTO documents (title, content, embedding) VALUES (?, ?, ?)", 
                 (title, text, embedding.tobytes()))

conn.commit()
print("✅ Data inserted successfully!")

# 4️⃣ Query
query = "Where does Alexandra study?"
query_vec = model.encode(query)

cursor = conn.execute("""
SELECT title, content, embedding <-> ? AS distance
FROM documents
ORDER BY distance ASC
LIMIT 3
""", (query_vec.tobytes(),))

print("\n🔍 Query Results:")
for row in cursor.fetchall():
    print(f"Title: {row[0]}, Distance: {row[2]:.4f}")
    print(f"Excerpt: {row[1][:150]}...\n")
