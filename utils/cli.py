

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
    print("Thank you for using the AI Blog Writing Agent!")
