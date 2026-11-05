from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os

ROOT = Path(__file__).resolve().parent.parent

load_dotenv(f"{ROOT}/.env")

os.getenv("HF_TOKEN")

class IntentCheck():
    def __init__(self) -> None:
        self.__model = SentenceTransformer('all-MiniLM-L6-v2')
        self.__anchor = {
            "GENERAL_CHAT":[
            "Can you write a Python script for quicksort?",
            "What is the difference between a list and a tuple in Python?",
            "Explain how async concurrency works in web frameworks",
            "Help me debug this traceback error code",
            "Tell me how transformer self-attention works",
            "How do I configure Nginx as a reverse proxy?",
            "What's the capital of France?",
            "Can you refactor this SQL query for better performance?"
        ],
            "JOURNAL_QUERIES": [
            "What did I write in my journal yesterday?",
            "Show me my past entries about FastAPI and Docker",
            "What notes did I take last week regarding database schemas?",
            "Summarize my thoughts on my recent machine learning projects",
            "Look up what I worked on previously",
            "Did I write anything about PyTorch tensors recently?",
            "Pull up my old journal notes on API rate limits",
            "What was my main takeaway from my dev log on Monday?"
        ]
        }
        self.__anchor_embeddings = {
            intent : self.__model.encode(sentence)
            for intent, sentence in self.__anchor.items()
        }
    def compare(self, prompt: str, threshold: float = 0.45):
        highest_score = -1
        best_intent = "GENERAL_CHAT"
        user_emb = self.__model.encode([prompt])
        for intent, embedding_matrix in self.__anchor_embeddings.items():
            similarity_score = cosine_similarity(user_emb, embedding_matrix)
            max_score_for_intent = np.max(similarity_score)
            if max_score_for_intent > highest_score:
                highest_score = max_score_for_intent
                best_intent = intent

        if highest_score < threshold:
            return "GENERAL_CHAT"

        return best_intent


if __name__ == "__main__":
    router = IntentCheck()
    
    test_msg = "Generate some text for me to create a Journal on the Ayurveda"
    result = router.compare(test_msg)
    
    print(f"\nUser Message: '{test_msg}'")
    print(f"Detected Intent: **{result}**")