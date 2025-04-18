import google.generativeai as genai
from dotenv import load_dotenv
import os
import re
import asyncio
from utils.api_handler import APIHandler

class ContextAgent:
    def __init__(self, topic, tone):
        self.topic = topic
        self.tone = tone
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        self.api_handler = APIHandler()

    def generate_subtopics(self):
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            f"Generate 4-5 subtopics (H2 headings) for a blog on '{self.tone}' "
            f"with a {self.tone} tone. Return only the headings as a numbered list, "
            f"one per line, without any additional text or formatting (e.g., no asterisks or explanations)."
            f"Example:\n1. Introduction to Python in AI\n2. Key Libraries for AI Development"
        )
        response = model.generate_content(prompt)
        subtopics = response.text.strip().split("\n")
        # Clean up: remove numbering and ensure only headings remain
        cleaned_subtopics = [
            re.sub(r"^\d+\.\s*", "", line).strip() 
            for line in subtopics 
            if line.strip() and re.match(r"^\d+\.", line)
        ]
        return cleaned_subtopics

    async def research(self):
        query = self.topic.lower().replace(" ", "+")
        research_data = await self.api_handler.fetch_all(query)
        return research_data