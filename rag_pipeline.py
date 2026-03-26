from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from data_loader import load_data
import os

class RAGPipeline:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.documents = load_data()
        self.index = None
        self.embeddings = None

        self.build_index()

    def build_index(self):
        self.embeddings = self.model.encode(self.documents)
        dim = self.embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(self.embeddings))

    def retrieve(self, query, k=3):
        q_emb = self.model.encode([query])
        distances, indices = self.index.search(q_emb, k)

        results = [self.documents[i] for i in indices[0]]
        return results

    def generate_response(self, query, llm="openai"):
        context = self.retrieve(query)

        prompt = f"""
        You are a marketing analytics assistant.

        Context:
        {context}

        Question:
        {query}

        Provide clear insights.
        """

        if llm == "openai":
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            return response.choices[0].message.content

        elif llm == "gemini":
            import google.generativeai as genai

            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel("gemini-pro")

            response = model.generate_content(prompt)
            return response.text

        elif llm == "deepseek":
            # HF inference (free tier)
            from huggingface_hub import InferenceClient

            client = InferenceClient("deepseek-ai/DeepSeek-R1")

            response = client.text_generation(prompt, max_new_tokens=300)
            return response

        else:
            return "Invalid LLM selected"
