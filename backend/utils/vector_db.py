import chromadb
from chromadb.utils import embedding_functions
import os
from datetime import datetime

class VectorDB:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="chroma_db")
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-ada-002"
        )
    
    def add_document(self, filename, content):
        """Add document to vector database"""
        # Split content into chunks
        chunks = self._chunk_text(content)
        
        # Generate embeddings and store
        self.collection.add(
            documents=chunks,
            metadatas=[{"source": filename} for _ in chunks],
            ids=[f"{filename}_{i}" for i in range(len(chunks))]
        )
    
    def query(self, query_text, n_results=3):
        """Query the vector database"""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            include=["documents", "metadatas"]
        )
        
        # Combine results from all chunks
        combined_text = ""
        for i in range(len(results['documents'][0])):
            combined_text += f"Document {results['metadatas'][0][i]['source']}:\n"
            combined_text += results['documents'][0][i] + "\n\n"
        
        return combined_text.strip()
    
    def _chunk_text(self, text, chunk_size=1000, overlap=100):
        """Split text into chunks for embedding"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
        
        return chunks
