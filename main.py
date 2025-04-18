import argparse
import os
from utils.cli import display_welcome, display_summary
from agents.context_agent import ContextAgent

def parse_arguments():
    parser = argparse.ArgumentParser(description="AI Blog Writing Agent")
    parser.add_argument("--topic", required=True, help="Blog topic (e.g., 'How Python is used in AI')")
    parser.add_argument("--tone", default="educational", 
                       choices=["educational", "formal", "creative", "technical"],
                       help="Tone of the blog (default: educational)")
    return parser.parse_args()

def main():
    args = parse_arguments()
    topic = args.topic
    tone = args.tone

    display_welcome(topic, tone)
    
    # Test Context Agent
    context_agent = ContextAgent(topic, tone)
    subtopics = context_agent.generate_subtopics()
    print("Generated Subtopics:")
    for subtopic in subtopics:
        print(f"- {subtopic}")
    
    display_summary(topic, "outputs/blogs/sample_blog.md", "outputs/metadata/sample_metadata.json")

if __name__ == "__main__":
    main()