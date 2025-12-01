import sqlite3
import sqlite_vec
import numpy as np

# ------------------------------
# SETUP: sample table + vectors
# ------------------------------
conn = sqlite3.connect(":memory:")
sqlite_vec.load(conn)

# If you are using a custom SQLite vector extension,
# you may need something like:
# conn.enable_load_extension(True)
# conn.load_extension("your_vector_extension.so")

conn.execute("""
CREATE TABLE books_vectors (
    id        INTEGER PRIMARY KEY,
    title     TEXT NOT NULL,
    embedding BLOB NOT NULL
);
""")

# Helper to create a fake 384-dim embedding
def make_vec(value: float) -> bytes:
    return np.array([value] * 384, dtype=np.float32).tobytes()

# Sample book vectors (fake data)
book1_emb = make_vec(0.10)   # Book 1
book2_emb = make_vec(0.80)   # Book 2 (far away)
book3_emb = make_vec(0.14)   # Book 3 (close to Book 1)

conn.executemany(
    "INSERT INTO books_vectors (id, title, embedding) VALUES (?, ?, ?)",
    [
        (1, "Book 1: Intro to AI",       book1_emb),
        (2, "Book 2: Cooking with Love", book2_emb),
        (3, "Book 3: Machine Learning",  book3_emb),
    ],
)
conn.commit()

# ------------------------------
# SEARCH: ask user for query text
# ------------------------------
def fake_text_embedding(text: str) -> bytes:
    """
    Demo: ignore text and just make a vector
    that is 'close' to Book 1 and Book 3.
    In real life, you would call your model here.
    """
    return np.array([0.15] * 384, dtype=np.float32).tobytes()

query_text = input("Enter your search text: ")
query_emb = fake_text_embedding(query_text)

# ------------------------------
# VECTOR SEARCH (top-2, cosine)
# ------------------------------
# NOTE: The exact SQL depends on your extension.
# This matches your original style:
cur = conn.execute(
    """
    SELECT id, title
    FROM books_vectors
    WHERE vec_search(?, 2, 'distance'='cosine')
    """,
    (query_emb,),
)

results = cur.fetchall()

print("Top-2 similar books:")
for row in results:
    print(row)

# Example of what you might see when running this
# (fake sample output):
# Top-2 similar books:
# (1, 'Book 1: Intro to AI')
# (3, 'Book 3: Machine Learning')