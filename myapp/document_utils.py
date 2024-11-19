from sentence_transformers import SentenceTransformer
import os

def process_document(file_path):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    with open(file_path, 'r') as file:
        content = file.read()
    embeddings = model.encode(content.split('.'))  # Chunk sentences
    return embeddings
