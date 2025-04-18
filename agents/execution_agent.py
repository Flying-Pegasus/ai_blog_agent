import os
import json

class ExecutionAgent:
    def __init__(self, topic, blog_content, metadata):
        self.topic = topic
        self.blog_content = blog_content
        self.metadata = metadata

    def export_blog(self):
        blog_path = f"outputs/blogs/{self.topic.lower().replace(' ', '_')}.md"
        os.makedirs(os.path.dirname(blog_path), exist_ok=True)
        with open(blog_path, "w", encoding="utf-8") as f:
            f.write(self.blog_content)
        return blog_path

    def export_metadata(self):
        metadata_path = f"outputs/metadata/{self.topic.lower().replace(' ', '_')}.json"
        os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2)
        return metadata_path