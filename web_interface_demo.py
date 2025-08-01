#!/usr/bin/env python3
"""
Demo script to show web interface capabilities and create sample blogs
"""

from blog_team_coordinator import BlogTeamCoordinator
import os
import webbrowser
import time

def create_sample_blogs():
    """Create sample blogs for web interface demo"""
    print("PREPARING WEB INTERFACE DEMO")
    print("=" * 50)
    
    coordinator = BlogTeamCoordinator()
    
    # Sample topics for demo
    demo_topics = [
        {
            "topic": "Web Development Best Practices 2024",
            "audience": "developers",
            "tone": "technical",
            "keywords": ["web development", "best practices", "coding"]
        },
        {
            "topic": "Digital Marketing Strategies for Small Business",
            "audience": "business owners", 
            "tone": "professional",
            "keywords": ["digital marketing", "small business", "marketing strategies"]
        },
        {
            "topic": "Beginner Guide to Artificial Intelligence",
            "audience": "beginners",
            "tone": "conversational", 
            "keywords": ["artificial intelligence", "AI", "machine learning"]
        }
    ]
    
    print("📝 Creating sample blogs for web interface...")
    created_blogs = []
    
    for i, blog_config in enumerate(demo_topics, 1):
        print(f"\n{i}. Creating: {blog_config['topic']}")
        
        result = coordinator.create_blog_post(
            topic=blog_config['topic'],
            target_audience=blog_config['audience'],
            tone=blog_config['tone'],
            word_count=1200,
            custom_keywords=blog_config['keywords']
        )
        
        created_blogs.append(result)
        print(f"   ✅ Created (SEO: {result['seo_score']}%)")
    
    return created_blogs

def show_blog_page_links(blogs):
    """Display blog page links"""
    print(f"\n🔗 BLOG PAGE LINKS")
    print("=" * 50)
    
    for i, blog in enumerate(blogs, 1):
        workflow_id = blog['workflow_id']
        blog_page_path = os.path.join("blog_output", workflow_id, "blog_page.html")
        
        if os.path.exists(blog_page_path):
            abs_path = os.path.abspath(blog_page_path)
            file_url = f"file:///{abs_path.replace(os.sep, '/')}"
            
            print(f"\n{i}. {blog['topic']}")
            print(f"   📄 File: {abs_path}")
            print(f"   🌐 URL:  {file_url}")
            print(f"   📊 SEO:  {blog['seo_score']}%")
            print(f"   📝 Words: {blog['word_count']}")

def launch_web_interface():
    """Instructions for launching web interface"""
    print(f"\n🚀 LAUNCH WEB INTERFACE")
    print("=" * 50)
    
    print("To start the web interface, run one of these commands:")
    print()
    print("Method 1 (Recommended):")
    print("   python run_app.py")
    print()
    print("Method 2 (Direct):")
    print("   streamlit run streamlit_app.py")
    print()
    print("📱 The web interface will open at: http://localhost:8501")
    print()
    print("🎯 Web Interface Features:")
    print("   ✅ Interactive blog creation form")
    print("   ✅ Real-time progress tracking")  
    print("   ✅ Professional UI with tabs")
    print("   ✅ SEO analytics dashboard")
    print("   ✅ Standalone blog page generation")
    print("   ✅ Direct blog page links")
    print("   ✅ Download options (MD, HTML)")
    print("   ✅ Existing blog management")
    print("   ✅ Content viewing and editing")

def show_file_structure():
    """Show the file structure for reference"""
    print(f"\n📁 PROJECT STRUCTURE")
    print("=" * 50)
    
    print("Key Files:")
    print("├── streamlit_app.py           # Main web interface")
    print("├── run_app.py                 # Easy launcher")
    print("├── blog_team_coordinator.py   # Core system")
    print("├── pages/")
    print("│   └── blog_viewer.py         # Additional page")
    print("└── blog_output/")
    print("    └── {workflow_id}/")
    print("        ├── blog_page.html     # ← MAIN BLOG PAGE")
    print("        ├── final_blog_post.md")
    print("        └── [other files...]")

def main():
    print("🌐 WEB INTERFACE DEMO PREPARATION")
    print("=" * 60)
    print("This script prepares sample content for the web interface demo")
    print()
    
    # Create sample blogs
    blogs = create_sample_blogs()
    
    # Show blog page links
    show_blog_page_links(blogs)
    
    # Show file structure
    show_file_structure()
    
    # Launch instructions
    launch_web_interface()
    
    print(f"\n🎉 DEMO PREPARATION COMPLETE!")
    print("=" * 60)
    print("✅ Sample blogs created")
    print("✅ Blog pages generated") 
    print("✅ Links ready for testing")
    print("✅ Web interface ready to launch")
    print()
    print("💡 Next step: Run 'python run_app.py' to start the web interface!")

if __name__ == "__main__":
    main()