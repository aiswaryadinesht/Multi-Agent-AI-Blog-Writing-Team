#!/usr/bin/env python3
"""
Test script that shows blog content in the output
"""

from blog_team_coordinator import BlogTeamCoordinator

def test_with_content_printing():
    print("MULTIAGENT BLOG WRITING SYSTEM - WITH CONTENT OUTPUT")
    print("=" * 60)
    
    coordinator = BlogTeamCoordinator()
    
    # Create a blog post - content will be printed automatically
    print("\nCreating blog post about 'Web Development Best Practices'...")
    
    result = coordinator.create_blog_post(
        topic="Web Development Best Practices",
        target_audience="junior developers",
        tone="conversational",
        word_count=1500,
        custom_keywords=["web development", "best practices", "coding"]
    )
    
    print(f"\nWorkflow completed! Files saved to: blog_output/{result['workflow_id']}/")
    
    # You can also print content from existing workflows
    print("\n" + "="*60)
    print("PRINTING CONTENT FROM PREVIOUS WORKFLOWS")
    print("="*60)
    
    # List all workflows
    workflows = coordinator.list_workflows()
    print(f"Found {len(workflows)} total workflows:")
    
    for i, workflow in enumerate(workflows, 1):
        print(f"{i}. {workflow['topic']} (SEO: {workflow['seo_score']}%)")
    
    # Print content from the latest workflow
    if workflows:
        print(f"\nShowing content from latest workflow:")
        coordinator.print_latest_workflow()

def test_individual_content_access():
    """
    Test accessing content from specific workflows
    """
    print("\n" + "="*60)
    print("INDIVIDUAL WORKFLOW CONTENT ACCESS")
    print("="*60)
    
    coordinator = BlogTeamCoordinator()
    workflows = coordinator.list_workflows()
    
    if len(workflows) >= 2:
        # Print content from the second workflow
        second_workflow = workflows[1]
        print(f"\nContent from workflow: {second_workflow['topic']}")
        coordinator.print_workflow_content(second_workflow['workflow_id'])
    else:
        print("Need at least 2 workflows to demonstrate individual access")

if __name__ == "__main__":
    test_with_content_printing()
    test_individual_content_access()