import google.generativeai as genai
from dotenv import load_dotenv
import os

class SEOAgent:
    def __init__(self, topic, tone, research_data, blog_content):
        self.topic = topic
        self.tone = tone
        self.research_data = research_data
        self.blog_content = blog_content
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_title(self):
        prompt = (
            f"Generate a concise, SEO-optimized blog title (max 60 characters) "
            f"for a blog on '{self.topic}' with a {self.tone} tone."
        )
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def generate_meta_description(self):
        keywords = ", ".join(self.generate_tags()[:3])
        prompt = (
            f"Write a 150-160 character meta-description for a blog on '{self.topic}' "
            f"with a {self.tone} tone. Include keywords: {keywords}. "
            f"Use clear, professional language to attract readers."
        )
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def generate_tags(self):
        # Filter keywords to exclude irrelevant terms
        valid_keywords = [
            kw for kw in self.research_data["keywords"]
            if len(kw.split()) <= 2 and kw.lower() not in [
                "three-toed sloth", "bradypus tridactylus", "petri", "anon", "mei", "chiu", "yee", "lian",
                "artificial insemination", "cbs", "nsis", "nih", "nsi", "establishment", "immigration", "without",
                "elected", "adherents", "advocates"
            ]
        ]
        return valid_keywords[:5] or ["AI", "Python", "machine learning", "data science", "neural network"]

    def calculate_reading_time(self):
        word_count = len(self.blog_content.split())
        minutes = round(word_count / 200)
        return max(1, minutes)

    def generate_url_slug(self):
        return self.topic.lower().replace(" ", "-").replace("'", "")

    def generate_metadata(self):
        return {
            "title": self.generate_title(),
            "meta_description": self.generate_meta_description(),
            "tags": self.generate_tags(),
            "reading_time_minutes": self.calculate_reading_time(),
            "url_slug": self.generate_url_slug()
        }