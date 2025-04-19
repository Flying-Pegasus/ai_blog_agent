def display_welcome(topic, tone):
    print("=====================================")
    print("      AI Blog Writing Agent      ")
    print("=====================================")
    print(f"Topic: {topic}")
    print(f"Tone: {tone}")
    print("Starting blog generation process...\n")

def display_summary(topic, blog_path, metadata_path):
    print("\n=====================================")
    print("           Process Complete           ")
    print("=====================================")
    print(f"Topic: {topic}")
    print(f"Blog saved to: {blog_path}")
    print(f"Metadata saved to: {metadata_path}")
    # Load metadata for summary
    try:
        with open(metadata_path, "r", encoding="utf-8") as f:
            import json
            metadata = json.load(f)
        print(f"Blog Title: {metadata['title']}")
        print(f"Meta Description: {metadata['meta_description']}")
        print(f"Tags: {', '.join(metadata['tags'])}")
        print(f"Reading Time: {metadata['reading_time_minutes']} minutes")
        print(f"URL Slug: {metadata['url_slug']}")
    except Exception as e:
        print(f"Error displaying metadata: {str(e)}")
    # Show quote used
    try:
        with open(blog_path, "r", encoding="utf-8") as f:
            blog_content = f.read()
            # Find quote between first H1 and first H2
            intro = blog_content.split("## ")[1] if len(blog_content.split("## ")) > 1 else blog_content
            for line in intro.split("\n"):
                if "\"" in line and " by " in line:
                    print(f"Quote Used: {line.strip()}")
                    break
            else:
                print("Quote Used: Not found in introduction")
    except Exception as e:
        print(f"Error displaying quote: {str(e)}")
    print("Thank you for using the AI Blog Writing Agent!")