#!/usr/bin/env python3
"""
Example Usage and Testing for Blog Writing Team Multiagent System

This script demonstrates how to use the multiagent blog writing system
with various configurations and scenarios.
"""

import os
import sys
from blog_team_coordinator import BlogTeamCoordinator

def demo_basic_workflow():
    """
    Demonstrate basic blog creation workflow
    """
    print("DEMO 1: Basic Blog Creation Workflow")
    print("="*60)
    
    coordinator = BlogTeamCoordinator()
    
    # Create a blog post about "Machine Learning"
    result = coordinator.create_blog_post(
        topic="Machine Learning for Beginners",
        target_audience="developers new to ML",
        tone="conversational",
        word_count=1800
    )
    
    print(f"\nBlog post created successfully!")
    print(f"SEO Score: {result['seo_score']}%")
    print(f"Word Count: {result['word_count']}")
    print(f"Output: blog_output/{result['workflow_id']}/")
    
    return result

def demo_professional_tone():
    """
    Demonstrate professional tone for B2B audience
    """
    print("\nDEMO 2: Professional B2B Content")
    print("="*60)
    
    coordinator = BlogTeamCoordinator()
    
    result = coordinator.create_blog_post(
        topic="Enterprise Software Security",
        target_audience="IT decision makers",
        tone="professional",
        word_count=2500,
        custom_keywords=["enterprise security", "software security", "cybersecurity"]
    )
    
    print(f"✅ Professional blog post created!")
    print(f"📊 SEO Score: {result['seo_score']}%")
    print(f"🎯 Target Audience: {result['target_audience']}")
    
    return result

def demo_technical_content():
    """
    Demonstrate technical content creation
    """
    print("\n🎯 DEMO 3: Technical Tutorial Content")
    print("="*60)
    
    coordinator = BlogTeamCoordinator()
    
    result = coordinator.create_blog_post(
        topic="Docker Container Optimization",
        target_audience="DevOps engineers",
        tone="technical",
        word_count=2200,
        custom_keywords=["docker optimization", "container performance", "devops"]
    )
    
    print(f"✅ Technical tutorial created!")
    print(f"🔧 Readability Score: {result['readability_score']}")
    print(f"⚡ Performance Prediction: {result['performance_prediction']['search_ranking_potential']}")
    
    return result

def demo_workflow_management():
    """
    Demonstrate workflow management features
    """
    print("\n🎯 DEMO 4: Workflow Management")
    print("="*60)
    
    coordinator = BlogTeamCoordinator()
    
    # List all existing workflows
    workflows = coordinator.list_workflows()
    print(f"📋 Found {len(workflows)} existing workflows:")
    
    for workflow in workflows[:3]:  # Show first 3
        print(f"  • {workflow['topic']} (Score: {workflow['seo_score']}%)")
    
    if workflows:
        # Check status of the first workflow
        first_workflow = workflows[0]
        status = coordinator.get_workflow_status(first_workflow['workflow_id'])
        print(f"\n📊 Status of '{first_workflow['topic']}':")
        print(f"  • Completed phases: {status['completed_phases']}")
        print(f"  • Status: {status['status']}")

def test_individual_agents():
    """
    Test each agent individually
    """
    print("\n🎯 DEMO 5: Individual Agent Testing")
    print("="*60)
    
    from content_researcher_agent import ContentResearcherAgent
    from content_writer_agent import ContentWriterAgent
    from seo_editor_agent import SEOEditorAgent
    
    # Test Research Agent
    print("\n🔍 Testing Research Agent...")
    researcher = ContentResearcherAgent()
    research_data = researcher.research_topic("Python Programming", "beginners")
    print(f"✅ Research completed: {len(research_data['trends'])} trends, {len(research_data['keywords'])} keywords")
    
    # Test Content Writer Agent
    print("\n✍️ Testing Content Writer Agent...")
    writer = ContentWriterAgent()
    content_data = writer.write_blog_post(research_data, "conversational", 1200)
    print(f"✅ Content written: {content_data['word_count']} words, {len(content_data['main_content'])} sections")
    
    # Test SEO Editor Agent
    print("\n🔧 Testing SEO Editor Agent...")
    seo_editor = SEOEditorAgent()
    optimized_data = seo_editor.optimize_content(content_data, research_data)
    print(f"✅ SEO optimization completed: {optimized_data['seo_score']['percentage']}% score")
    print(f"📈 Performance prediction: {optimized_data['performance_predictions']['search_ranking_potential']}")

def performance_comparison():
    """
    Compare performance across different configurations
    """
    print("\n🎯 DEMO 6: Performance Comparison")
    print("="*60)
    
    coordinator = BlogTeamCoordinator()
    
    topics = [
        ("AI in Healthcare", "healthcare professionals", "professional"),
        ("Social Media Marketing Tips", "small business owners", "conversational"),
        ("Cloud Computing Architecture", "software architects", "technical")
    ]
    
    results = []
    
    for topic, audience, tone in topics:
        print(f"\n📝 Creating: {topic}")
        result = coordinator.create_blog_post(
            topic=topic,
            target_audience=audience,
            tone=tone,
            word_count=1500
        )
        
        results.append({
            "topic": topic,
            "seo_score": result["seo_score"],
            "word_count": result["word_count"],
            "readability": result["readability_score"],
            "tone": tone
        })
        
        print(f"  ✅ SEO: {result['seo_score']}% | Words: {result['word_count']} | Readability: {result['readability_score']}")
    
    # Show comparison
    print(f"\n📊 PERFORMANCE COMPARISON:")
    print(f"{'Topic':<30} {'SEO':<6} {'Words':<6} {'Readability':<12} {'Tone':<12}")
    print("-" * 70)
    
    for result in results:
        print(f"{result['topic'][:29]:<30} {result['seo_score']:<6}% {result['word_count']:<6} {result['readability']:<12} {result['tone']:<12}")

def export_sample_files():
    """
    Export sample files for demonstration
    """
    print("\n🎯 DEMO 7: Export Sample Files")
    print("="*60)
    
    coordinator = BlogTeamCoordinator()
    
    # Create a comprehensive blog post
    result = coordinator.create_blog_post(
        topic="Complete Guide to Remote Work Productivity",
        target_audience="remote workers",
        tone="conversational",
        word_count=2000,
        custom_keywords=["remote work", "productivity", "work from home", "remote productivity"]
    )
    
    workflow_dir = f"blog_output/{result['workflow_id']}"
    
    print(f"\n📁 Sample files created in: {workflow_dir}/")
    print("📄 Files included:")
    
    expected_files = [
        "final_blog_post.md",
        "seo_ready.html", 
        "workflow_summary.json",
        "optimization_report.txt",
        "content_brief.md",
        "research_data.json",
        "content_data.json",
        "seo_data.json"
    ]
    
    for filename in expected_files:
        filepath = os.path.join(workflow_dir, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"  ✅ {filename} ({size:,} bytes)")
        else:
            print(f"  ❌ {filename} (missing)")

def main():
    """
    Run all demonstrations
    """
    print("🚀 MULTIAGENT BLOG WRITING SYSTEM - DEMO SUITE")
    print("="*70)
    print("This demo showcases the complete blog writing workflow using AI agents.")
    print("Each agent specializes in research, writing, and SEO optimization.\n")
    
    try:
        # Run demonstrations
        demo_basic_workflow()
        demo_professional_tone()
        demo_technical_content()
        demo_workflow_management()
        test_individual_agents()
        performance_comparison()
        export_sample_files()
        
        print("\n🎉 ALL DEMOS COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("📁 Check the 'blog_output' directory for all generated content.")
        print("🔧 Review the optimization reports for SEO insights.")
        print("📊 Analyze the workflow summaries for performance metrics.")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {str(e)}")
        print("💡 Make sure all required dependencies are installed.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)