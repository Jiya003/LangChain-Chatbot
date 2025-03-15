import json
import numpy as np
import faiss
import torch
from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer
from flask_cors import CORS

app = Flask(__name__, template_folder="templates", static_folder="static")  
CORS(app)

# Load course data
try:
    with open("courses.json", "r", encoding="utf-8") as f:
        courses = json.load(f)
except FileNotFoundError:
    print("Error: 'courses.json' file not found.")
    courses = []

# Load FAISS index
try:
    index = faiss.read_index("course_embeddings.index")
except Exception as e:
    print(f"Error loading FAISS index: {e}")
    index = None

# Load embedding model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer("all-MiniLM-L6-v2", device=device)

# Search function
def search_courses(query, top_k=5):
    if index is None or len(courses) == 0:
        return []

    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        if 0 <= idx < len(courses):
            results.append(courses[idx])

    return results

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")  # Serve the chatbot UI

@app.route("/search", methods=["GET"])
def handle_query():
    user_input = request.args.get("query")
    if not user_input:
        return jsonify({"error": "Query parameter is required"}), 400

    results = search_courses(user_input)
    return jsonify({"results": results})

@app.route("/favicon.ico")
def favicon():
    return "", 204  # No Content

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Route not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
