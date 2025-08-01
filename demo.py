#!/usr/bin/env python3
"""
Demo script for the multiagent blog writing system
"""

from blog_team_coordinator import BlogTeamCoordinator

def run_demos():
    print("MULTIAGENT BLOG WRITING SYSTEM - DEMO")
    print("=" * 50)
    
    coordinator = BlogTeamCoordinator()
    
    # Demo 1: Basic blog creation
    print("\nDEMO 1: Basic Blog Creation")
    print("-" * 30)
    
    result1 = coordinator.create_blog_post(
        topic="Machine Learning Basics",
        target_audience="developers",
        tone="conversational",
        word_count=1500
    )
    
    print(f"Title: {result1['final_title']}")
    print(f"SEO Score: {result1['seo_score']}%")
    print(f"Word Count: {result1['word_count']}")
    
    # Demo 2: Professional content
    print("\n\nDEMO 2: Professional B2B Content")
    print("-" * 30)
    
    result2 = coordinator.create_blog_post(
        topic="Enterprise Data Security",
        target_audience="IT managers",
        tone="professional",
        word_count=2000,
        custom_keywords=["data security", "enterprise", "cybersecurity"]
    )
    
    print(f"Title: {result2['final_title']}")
    print(f"SEO Score: {result2['seo_score']}%")
    print(f"Target Audience: {result2['target_audience']}")
    
    # Demo 3: List existing workflows
    print("\n\nDEMO 3: Workflow Management")
    print("-" * 30)
    
    workflows = coordinator.list_workflows()
    print(f"Total workflows created: {len(workflows)}")
    
    for i, workflow in enumerate(workflows[:3], 1):
        print(f"{i}. {workflow['topic']} (SEO: {workflow['seo_score']}%)")
    
    print("\n" + "=" * 50)
    print("DEMOS COMPLETED SUCCESSFULLY!")
    print("Check the 'blog_output' directory for all generated content.")

if __name__ == "__main__":
    run_demos()