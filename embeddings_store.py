import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Load extracted courses
with open("courses.json", "r", encoding="utf-8") as f:
    courses = json.load(f)

# Initialize the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")  # Small but efficient model

# Extract text for embedding
texts = [
    f"{course.get('title', 'N/A')} {course.get('detailed_description', 'N/A')} "
    f"{course.get('price_per_session', 'N/A')} {course.get('number_of_lessons', 'N/A')} "
    f"{course.get('duration', 'N/A')} {course.get('total_price', 'N/A')} "
    f"{course.get('course_link', 'N/A')}"
    for course in courses
]

# Generate embeddings
embeddings = model.encode(texts, convert_to_numpy=True)

# Store embeddings in FAISS
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)  # L2 Distance Index
index.add(embeddings)  # Add embeddings to FAISS

# Save FAISS index
faiss.write_index(index, "course_embeddings.index")

print("Embeddings generated and stored successfully!")
