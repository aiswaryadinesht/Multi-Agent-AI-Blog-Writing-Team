#!/usr/bin/env python3
"""
Simple test for the multiagent blog writing system
"""

from blog_team_coordinator import BlogTeamCoordinator

def simple_test():
    print("Testing Multiagent Blog Writing System")
    print("="*50)
    
    try:
        # Initialize coordinator
        coordinator = BlogTeamCoordinator()
        print("Coordinator initialized successfully")
        
        # Create a simple blog post
        print("\nCreating blog post...")
        result = coordinator.create_blog_post(
            topic="Python Programming Tips",
            target_audience="beginner developers",
            tone="conversational",
            word_count=1200
        )
        
        print(f"SUCCESS!")
        print(f"Title: {result['final_title']}")
        print(f"Word Count: {result['word_count']}")
        print(f"SEO Score: {result['seo_score']}%")
        print(f"Output Directory: blog_output/{result['workflow_id']}/")
        
        # The blog content was already printed by the coordinator
        print("\n[Blog content was displayed above during creation]")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = simple_test()
    if success:
        print("\nTest completed successfully!")
    else:
        print("\nTest failed!")