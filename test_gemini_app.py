import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configure Gemini API
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")  # Updated model name

# Test content generation
prompt = "What is my name"
response = model.generate_content(prompt)
print("Generated Content:")
print(response.text)