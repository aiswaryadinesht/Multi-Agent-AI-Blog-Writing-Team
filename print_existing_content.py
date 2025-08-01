#!/usr/bin/env python3
"""
Script to print content from existing blog workflows
"""

from blog_team_coordinator import BlogTeamCoordinator

def print_all_existing_content():
    print("EXISTING BLOG CONTENT VIEWER")
    print("=" * 50)
    
    coordinator = BlogTeamCoordinator()
    workflows = coordinator.list_workflows()
    
    if not workflows:
        print("No existing workflows found. Create some blogs first!")
        return
    
    print(f"Found {len(workflows)} workflows:\n")
    
    # List all workflows with numbers
    for i, workflow in enumerate(workflows, 1):
        creation_date = workflow['creation_date'].split('T')[0]  # Just the date part
        print(f"{i}. {workflow['topic']}")
        print(f"   - SEO Score: {workflow['seo_score']}%")
        print(f"   - Word Count: {workflow['word_count']} words") 
        print(f"   - Created: {creation_date}")
        print()
    
    # Print content from each workflow
    for i, workflow in enumerate(workflows, 1):
        print(f"\n{'='*60}")
        print(f"CONTENT #{i}: {workflow['topic'].upper()}")
        print('='*60)
        coordinator.print_workflow_content(workflow['workflow_id'])
        
        if i < len(workflows):
            input("\nPress Enter to see next blog content...")

def print_latest_content_only():
    """
    Just print the latest blog content 
    """
    print("LATEST BLOG CONTENT")
    print("=" * 40)
    
    coordinator = BlogTeamCoordinator()
    coordinator.print_latest_workflow()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--latest":
        print_latest_content_only()
    else:
        print_all_existing_content()