from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from typing import Dict, Optional

ROOT = Path(__file__).resolve().parent.parent

load_dotenv(f"{ROOT}/.env")


class PromptGeneration():
    def __init__(self) -> None:
        self.__client = Groq()
        self.__system_prompt = {
            "GENERAL_CHAT": (
                "You are DevJournal AI, an elite AI engineering and software development collaborator. "
                "Your primary purpose is to generate high-quality, precise, and articulate code, technical text, "
                "architecture explanations, and drafts requested by the user. "
                "Be direct, highly technical, and concise. Avoid unnecessary conversational filler, meta-talk, "
                "or generic AI introductory remarks; dive straight into the requested solution or content.",
                "Try to give the response under 1024 tokens"
            ),
            "JOURNAL_QUERIES": (
                "You are DevJournal AI, a personal journaling and knowledge management assistant. "
                "Your job is to analyze the user's past journal entry, notes, tags, and comments provided in the context below "
                "and generate written reflections, continuations, summaries, or insights based strictly on that record. "
                "CRITICAL INSTRUCTIONS: "
                "1. If a journal entry is provided in the context, you MUST use it immediately and directly. "
                "2. NEVER ask the user which journal they are referring to, and NEVER ask clarifying questions when data is present. "
                "3. NEVER use conversational filler like 'Sure thing!' or 'Could you let me know which journal...'. "
                "4. Fulfill the user's prompt instantly by synthesizing the title, content, tags, and comments provided."
                "5. Try to give the response under 1024 tokens"
            )
        }
    def build_messages(self, intent:str, user_query:str, retrieved_logs : Optional[Dict], journal_title:str):
        
        system_content = self.__system_prompt.get(intent, self.__system_prompt['GENERAL_CHAT'])
        
        if intent == "JOURNAL_QUERIES" and retrieved_logs:
            journal_content = retrieved_logs["content"]
            formatted_logs = f"""Title - {journal_title},
            content - {journal_content}"""
            user_content = (
                f"Here are the journal entries:\n{formatted_logs}\n\n"
                f"Based on these, generate text regarding: {user_query}"
            )
        else:
            user_content = f"""
                topic - {journal_title}
                prompt - {user_query}. Generate a perfect title and content for this topic."""

        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    def text_generation(self, message_payload: list):

        response = self.__client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=message_payload,
            temperature=0.7,
            max_tokens=1024,
            top_p=1.0
        )
        generated_text = response.choices[0].message.content

        return generated_text
