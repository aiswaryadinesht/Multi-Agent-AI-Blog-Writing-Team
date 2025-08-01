#!/usr/bin/env python3
"""
Simple demo for web interface - no unicode characters
"""

from blog_team_coordinator import BlogTeamCoordinator
import os

def main():
    print("WEB INTERFACE DEMO")
    print("=" * 50)
    
    print("Creating a sample blog for web interface...")
    
    coordinator = BlogTeamCoordinator()
    
    # Create one sample blog
    result = coordinator.create_blog_post(
        topic="Getting Started with AI Tools",
        target_audience="beginners",
        tone="conversational",
        word_count=1200,
        custom_keywords=["AI tools", "artificial intelligence", "beginner guide"]
    )
    
    print(f"Blog created successfully!")
    print(f"SEO Score: {result['seo_score']}%")
    print(f"Word Count: {result['word_count']}")
    
    # Show blog page link
    workflow_id = result['workflow_id']
    blog_page_path = os.path.join("blog_output", workflow_id, "blog_page.html")
    
    if os.path.exists(blog_page_path):
        abs_path = os.path.abspath(blog_page_path)
        file_url = f"file:///{abs_path.replace(os.sep, '/')}"
        
        print(f"\nBLOG PAGE CREATED:")
        print(f"File: {abs_path}")
        print(f"URL:  {file_url}")
        print(f"\nTo view: Double-click the HTML file or copy the URL to your browser")
    
    print(f"\nWEB INTERFACE LAUNCH:")
    print("To start the web interface:")
    print("1. Run: python run_app.py")
    print("2. Or: streamlit run streamlit_app.py")
    print("3. Open: http://localhost:8501")
    
    print(f"\nWEB INTERFACE FEATURES:")
    print("- Interactive blog creation")
    print("- Real-time progress tracking")
    print("- SEO analytics dashboard")
    print("- Standalone blog pages")
    print("- Content management")
    print("- Download options")
    
    print(f"\nDemo completed! Ready to launch web interface.")

if __name__ == "__main__":
    main()