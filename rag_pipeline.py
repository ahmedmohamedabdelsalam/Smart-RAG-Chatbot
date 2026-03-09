import os
from typing import Optional

import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Optional: Add dotenv support to load .env variables locally
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class RAGPipeline:
    def __init__(self):
        # Initialize Gemini Client
        self.gemini_api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        if not self.gemini_api_key:
            print("WARNING: GOOGLE_GEMINI_API_KEY is not set. RAG endpoints will not function.")
        else:
            genai.configure(api_key=self.gemini_api_key)

        # Initialize Qdrant Client
        # Using memory-based Qdrant for simplicity in this template, 
        # or connect to a real instance if QDRANT_URL is provided.
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        
        if qdrant_url:
            self.qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        else:
            print("WARNING: QDRANT_URL not set. Using in-memory Qdrant client for demonstration.")
            self.qdrant_client = QdrantClient(":memory:")
            
        self.collection_name = os.getenv("QDRANT_COLLECTION", "knowledge_base")
        
        # Automatically ingest local data.txt if it exists
        self._ingest_local_data()

    def _ingest_local_data(self):
        """Reads data.txt if it exists and uploads it to the Qdrant memory collection."""
        if not self.gemini_api_key:
            print("Skipping data.txt ingestion: Gemini API key not configured.")
            return
            
        # Use absolute path relative to this file's location
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_file = os.path.join(base_dir, "data.txt")
        print(f"Looking for data file at: {data_file}")
        
        if not os.path.exists(data_file):
            print("No data.txt file found. Skipping ingestion.")
            return
            
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                text = f.read().strip()
                
            if not text:
                return

            chunks = text.split("\n\n")
            chunks = [c.strip() for c in chunks if c.strip()]
            
            if not chunks: 
                return

            print(f"Ingesting {len(chunks)} chunks from {data_file} into Qdrant...")
            
            collections_response = self.qdrant_client.get_collections()
            collection_exists = any(c.name == self.collection_name for c in collections_response.collections)
            
            # Create collection if it doesn't exist (gemini-embedding-001 is 3072 dims)
            if not collection_exists:
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
                )

            points = []
            for i, chunk in enumerate(chunks):
                embedding = genai.embed_content(
                    model="models/gemini-embedding-001",
                    content=chunk,
                    task_type="retrieval_document",
                )
                points.append(
                    PointStruct(
                        id=i,
                        vector=embedding['embedding'],
                        payload={"text": chunk}
                    )
                )
            
            if points:
                self.qdrant_client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )
                print(f"Successfully ingested {len(points)} chunks into '{self.collection_name}'.")

        except Exception as e:
            print(f"Error reading or ingesting {data_file}: {e}")

    def retrieve_context(self, question: str, max_results: int = 3) -> str:
        """
        Retrieves relevant context from Qdrant using Gemini embeddings.
        """
        if not self.gemini_api_key:
            return "No context available (Gemini API key missing)."

        try:
            # Generate embedding for the question
            embedding = genai.embed_content(
                model="models/gemini-embedding-001",
                content=question,
                task_type="retrieval_query",
            )
            query_embedding = embedding['embedding']

            # Check if collection exists (important for in-memory or empty first-starts)
            collections_response = self.qdrant_client.get_collections()
            collection_exists = any(c.name == self.collection_name for c in collections_response.collections)
            
            if not collection_exists:
                return "The knowledge base is currently empty."

            # Search Qdrant (using query_points, compatible with newer qdrant_client versions)
            search_response = self.qdrant_client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=max_results
            )
            search_results = search_response.points

            # Combine retrieved texts
            contexts = [hit.payload.get("text", "") for hit in search_results if hit.payload]
            if contexts:
                return "\n\n".join(contexts)
            return "No relevant context found in the knowledge base."

        except Exception as e:
            print(f"Error retrieving context: {e}")
            return f"Error retrieving context: {e}"

    def ask(self, question: str) -> str:
        """
        Processes a question through the RAG pipeline.
        """
        if not self.gemini_api_key:
            return "Configuration Error: GOOGLE_GEMINI_API_KEY is not set. Please get a free API key from Google AI Studio."

        # 1. Retrieve Context
        context = self.retrieve_context(question, max_results=10)

        # 2. Construct Prompt
        system_prompt = (
            "You are a helpful and intelligent assistant.\n"
            "Use the provided context to answer the user's question.\n"
            "If the context doesn't contain the answer, say you don't know based on the provided information, "
            "but you can try to answer from your general knowledge if appropriate.\n"
            "Keep the answer concise and relevant."
        )
        
        user_message = f"Context:\n{context}\n\nQuestion:\n{question}"

        # 3. Generate Answer
        try:
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                system_instruction=system_prompt,
            )
            response = model.generate_content(
                user_message,
                generation_config=genai.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=1000,
                )
            )
            return response.text or "Error: Empty response from model."
        except Exception as e:
            print(f"Error generating answer: {e}")
            return f"Failed to generate answer due to an internal error: {e}"

# Global instance for the FastAPI app
rag_pipeline = RAGPipeline()
