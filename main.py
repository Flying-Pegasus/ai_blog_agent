import argparse
import os
import asyncio
from utils.cli import display_welcome, display_summary
from agents.context_agent import ContextAgent
from agents.writing_agent import WritingAgent
from agents.seo_agent import SEOAgent
from agents.execution_agent import ExecutionAgent

def parse_arguments():
    parser = argparse.ArgumentParser(description="AI Blog Writing Agent")
    parser.add_argument("--topic", required=True, help="Blog topic (e.g., 'How Python is used in AI')")
    parser.add_argument("--tone", default="educational", 
                       choices=["educational", "formal", "creative", "technical"],
                       help="Tone of the blog (default: educational)")
    return parser.parse_args()

async def main():
    args = parse_arguments()
    topic = args.topic
    tone = args.tone

    display_welcome(topic, tone)
    
    # Context Agent: Generate subtopics and research
    context_agent = ContextAgent(topic, tone)
    subtopics = context_agent.generate_subtopics()
    print("Generated Subtopics:")
    for subtopic in subtopics:
        print(f"- {subtopic}")
    
    research_data = await context_agent.research()
    print("\nResearch Data:")
    print(f"News Articles: {len(research_data['news'])} found")
    print(f"Keywords: {research_data['keywords']}")
    print(f"Quotes: {research_data['quotes']}")
    
    # Writing Agent: Generate blog
    writing_agent = WritingAgent(topic, tone, subtopics, research_data)
    blog_content = writing_agent.generate_blog()
    
    # SEO Agent: Generate metadata
    seo_agent = SEOAgent(topic, tone, research_data, blog_content)
    metadata = seo_agent.generate_metadata()
    
    # Execution Agent: Export blog and metadata
    execution_agent = ExecutionAgent(topic, blog_content, metadata)
    blog_path = execution_agent.export_blog()
    metadata_path = execution_agent.export_metadata()
    
    print("\nGenerated Blog Preview (first 1000 characters):")
    print(blog_content[:1000] + "..." if len(blog_content) > 1000 else blog_content)
    
    display_summary(topic, blog_path, metadata_path)

if __name__ == "__main__":
    asyncio.run(main())