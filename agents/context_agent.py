import google.generativeai as genai
from dotenv import load_dotenv
import os

class ContextAgent:
    def __init__(self, topic, tone):
        self.topic = topic
        self.tone = tone
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)

    def generate_subtopics(self):
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Suggest 4-5 subtopics (H2 headings) for a blog on '{self.topic}' with a {self.tone} tone."
        response = model.generate_content(prompt)
        subtopics = response.text.split("\n")
        return [s.strip() for s in subtopics if s.strip()]

    def research(self):
        # TODO: Integrate NewsData.io, Datamuse, Quotable.io
        pass