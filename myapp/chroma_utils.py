from chromadb.config import Settings
from chromadb import Client
from transformers import pipeline
import re


# Initialize Chroma client and create collection
client = Client(Settings())
collection = client.create_collection('chatbot_embeddings')

# Function to store embeddings
def store_embeddings(chatbot_id, embeddings):
    for i, emb in enumerate(embeddings):
        collection.add(
            documents=[f"chunk-{i}"],  # Document identifier
            metadatas=[{"chatbot_id": chatbot_id}],  # Metadata (e.g., chatbot id)
            embeddings=[emb]  # Embedding vector
        )

def fetch_relevant_chunks(chatbot_id, query):
    results = collection.query(
        query_texts=[query],
        n_results=5,
        where={"chatbot_id": chatbot_id}
    )
    return " ".join([res["document"] for res in results])


generator = pipeline('text-generation', model='gpt2')



def preprocess_document(content):
    # Clean and split content into manageable chunks
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', content)
    return [sentence.strip() for sentence in sentences if sentence.strip()]

def generate_response(prompt, context):
    full_prompt = f"{context}\n\nUser: {prompt}\nBot:"
    return generator(full_prompt, max_length=50)[0]['generated_text']
