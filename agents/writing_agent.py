import google.generativeai as genai
from dotenv import load_dotenv
import os

class WritingAgent:
    def __init__(self, topic, tone, subtopics, research_data):
        self.topic = topic
        self.tone = tone
        self.subtopics = subtopics
        self.research_data = research_data
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_introduction(self):
        # Select the first quote if available, otherwise use default
        quote = self.research_data["quotes"][0] if self.research_data["quotes"] else {
            "content": "Python powers AI innovation.",
            "author": "Anonymous",
            "source": "default"
        }
        prompt = (
            f"Write a 100-150 word introduction for a blog titled '{self.topic}' with a {self.tone} tone. "
            f"Include this quote: '{quote['content']}' by {quote['author']}. "
            f"Introduce the topic, its importance, and preview the subtopics: {', '.join(self.subtopics)}. "
            f"End with a hook to engage readers. Use clear, concise language suitable for beginners."
        )
        response = self.model.generate_content(prompt)
        introduction = response.text.strip()
        # Add ZenQuotes.io attribution if needed
        if quote.get("source") == "zenquotes.io":
            introduction += "\n\n*Inspirational quote provided by [ZenQuotes API](https://zenquotes.io/).*"
        return introduction

    def generate_section(self, subtopic):
        keywords = ", ".join(self.research_data["keywords"][:3] or ["AI", "Python", "machine learning"])
        prompt = (
            f"Write a 200-300 word section for a blog on '{self.topic}' with a {self.tone} tone, "
            f"titled '{subtopic}'. Incorporate these keywords: {keywords}. "
            f"Use clear, engaging language suitable for beginners. Include 2-3 bullet points summarizing key points. "
            f"Provide practical examples (e.g., Python libraries or AI applications) to make the content relatable."
        )
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def generate_conclusion(self):
        prompt = (
            f"Write a 100-150 word conclusion for a blog titled '{self.topic}' with a {self.tone} tone. "
            f"Summarize the key points from the subtopics: {', '.join(self.subtopics)}. "
            f"Include a call-to-action encouraging readers to explore Python for AI or share their experiences. "
            f"Use an inspiring and motivating tone."
        )
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def generate_blog(self):
        # Generate blog content
        introduction = self.generate_introduction()
        sections = [self.generate_section(subtopic) for subtopic in self.subtopics]
        conclusion = self.generate_conclusion()

        # Format in Markdown
        markdown = f"# {self.topic}\n\n"
        markdown += f"{introduction}\n\n"
        for subtopic, section in zip(self.subtopics, sections):
            markdown += f"## {subtopic}\n\n{section}\n\n"
        markdown += f"## Conclusion\n\n{conclusion}\n"
        return markdown