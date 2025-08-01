from typing import Dict, List, Optional
import json
from datetime import datetime
import os
import re

from content_researcher_agent import ContentResearcherAgent
from content_writer_agent import ContentWriterAgent
from seo_editor_agent import SEOEditorAgent

class BlogTeamCoordinator:
    """
    Coordinates the workflow between Research, Writing, and SEO agents
    Manages the complete blog creation process from topic to published content
    """
    
    def __init__(self, output_dir: str = "blog_output"):
        self.researcher = ContentResearcherAgent()
        self.writer = ContentWriterAgent()
        self.seo_editor = SEOEditorAgent()
        self.output_dir = output_dir
        self.workflow_data = {}
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def create_blog_post(self, topic: str, target_audience: str = "general", 
                        tone: str = "conversational", word_count: int = 1500,
                        custom_keywords: Optional[list] = None) -> Dict:
        """
        Complete workflow: Research → Write → Optimize
        """
        print(f"Starting blog creation workflow for: {topic}")
        print("=" * 50)
        
        workflow_id = self._generate_workflow_id(topic)
        
        # Phase 1: Research
        print("\nPHASE 1: RESEARCH")
        research_data = self.researcher.research_topic(topic, target_audience)
        self._save_phase_data(workflow_id, "research", research_data)
        print(f"Research completed: {len(research_data['trends'])} trends, {len(research_data['statistics'])} stats")
        
        # Phase 2: Content Writing
        print("\nPHASE 2: CONTENT WRITING")
        content_data = self.writer.write_blog_post(research_data, tone, word_count)
        self._save_phase_data(workflow_id, "content", content_data)
        print(f"Content written: {content_data['word_count']} words, {len(content_data['main_content'])} sections")
        
        # Phase 3: SEO Optimization
        print("\nPHASE 3: SEO OPTIMIZATION")
        keywords = custom_keywords or [kw["keyword"] for kw in research_data.get("keywords", [])]
        optimized_data = self.seo_editor.optimize_content(content_data, research_data, keywords)
        self._save_phase_data(workflow_id, "seo", optimized_data)
        print(f"SEO optimization completed: {optimized_data['seo_score']['percentage']}% score")
        
        # Compile final results
        final_output = self._compile_final_output(workflow_id, research_data, 
                                                content_data, optimized_data)
        
        # Export everything
        self._export_complete_workflow(workflow_id, final_output)
        
        # Create blog page HTML file
        self._create_blog_page_file(workflow_id, final_output)
        
        print(f"\nBlog post creation completed!")
        print(f"All files saved to: {self.output_dir}/{workflow_id}/")
        
        # Print the generated blog content
        self._print_blog_content(final_output)
        
        return final_output
    
    def _generate_workflow_id(self, topic: str) -> str:
        """
        Generate unique workflow ID
        """
        # Clean topic for filename
        clean_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
        clean_topic = clean_topic.replace(' ', '_').lower()[:30]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{clean_topic}_{timestamp}"
    
    def _save_phase_data(self, workflow_id: str, phase: str, data: Dict) -> None:
        """
        Save data from each phase
        """
        workflow_dir = os.path.join(self.output_dir, workflow_id)
        os.makedirs(workflow_dir, exist_ok=True)
        
        filepath = os.path.join(workflow_dir, f"{phase}_data.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
    
    def _compile_final_output(self, workflow_id: str, research_data: Dict, 
                            content_data: Dict, optimized_data: Dict) -> Dict:
        """
        Compile all phases into final output
        """
        return {
            "workflow_id": workflow_id,
            "creation_date": datetime.now().isoformat(),
            "topic": research_data["topic"],
            "target_audience": research_data["target_audience"],
            "final_title": optimized_data["seo_optimized_title"]["optimized"],
            "final_meta_description": optimized_data["optimized_meta_description"]["optimized"],
            "final_content": optimized_data["final_content"],
            "word_count": content_data["word_count"],
            "seo_score": optimized_data["seo_score"]["percentage"],
            "readability_score": optimized_data["readability_improvements"]["readability_score"],
            "performance_prediction": optimized_data["performance_predictions"],
            "research_summary": {
                "trends_found": len(research_data["trends"]),
                "statistics_collected": len(research_data["statistics"]),
                "expert_opinions": len(research_data["expert_opinions"]),
                "content_angles": len(research_data["content_angles"])
            },
            "optimization_summary": {
                "seo_grade": optimized_data["seo_score"]["grade"],
                "technical_seo_passed": optimized_data["technical_seo"]["passed"],
                "internal_links_suggested": len(optimized_data["internal_links"]),
                "external_links_suggested": len(optimized_data["external_links"])
            }
        }
    
    def _export_complete_workflow(self, workflow_id: str, final_output: Dict) -> None:
        """
        Export all final files
        """
        workflow_dir = os.path.join(self.output_dir, workflow_id)
        
        # Export final blog post (markdown)
        blog_path = os.path.join(workflow_dir, "final_blog_post.md")
        with open(blog_path, 'w', encoding='utf-8') as f:
            f.write(final_output["final_content"])
        
        # Export SEO-ready HTML version
        html_path = os.path.join(workflow_dir, "seo_ready.html")
        self._create_html_version(final_output, html_path)
        
        # Export workflow summary
        summary_path = os.path.join(workflow_dir, "workflow_summary.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(final_output, f, indent=2, default=str)
        
        # Export optimization report
        report_path = os.path.join(workflow_dir, "optimization_report.txt")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(self.seo_editor.generate_optimization_report())
        
        # Export content brief for client/team
        brief_path = os.path.join(workflow_dir, "content_brief.md")
        self._create_content_brief(final_output, brief_path)
    
    def _create_html_version(self, final_output: Dict, filepath: str) -> None:
        """
        Create SEO-ready HTML version
        """
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{final_output['final_title']}</title>
    <meta name="description" content="{final_output['final_meta_description']}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{final_output['final_title']}">
    <meta property="og:description" content="{final_output['final_meta_description']}">
    <meta property="og:type" content="article">
</head>
<body>
    <article>
        {self._markdown_to_html(final_output['final_content'])}
    </article>
</body>
</html>"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_template)
    
    def _markdown_to_html(self, markdown_content: str) -> str:
        """
        Simple markdown to HTML conversion
        """
        html = markdown_content
        
        # Convert headers
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        
        # Convert bold text
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        
        # Convert paragraphs
        paragraphs = html.split('\n\n')
        html_paragraphs = []
        for para in paragraphs:
            if para.strip() and not para.startswith('<h'):
                html_paragraphs.append(f'<p>{para.strip()}</p>')
            else:
                html_paragraphs.append(para)
        
        return '\n'.join(html_paragraphs)
    
    def _create_content_brief(self, final_output: Dict, filepath: str) -> None:
        """
        Create content brief for team/client review
        """
        brief = f"""# Content Brief: {final_output['topic']}

## Overview
- **Topic**: {final_output['topic']}
- **Target Audience**: {final_output['target_audience']}
- **Word Count**: {final_output['word_count']} words
- **SEO Score**: {final_output['seo_score']}% (Grade: {final_output['optimization_summary']['seo_grade']})
- **Readability**: {final_output['readability_score']}

## Performance Predictions
- **Search Ranking Potential**: {final_output['performance_prediction']['search_ranking_potential']}
- **Estimated Traffic**: {final_output['performance_prediction']['estimated_organic_traffic']}
- **Engagement Potential**: {final_output['performance_prediction']['engagement_potential']}

## Research Summary
- **Trends Analyzed**: {final_output['research_summary']['trends_found']}
- **Statistics Collected**: {final_output['research_summary']['statistics_collected']}
- **Expert Opinions**: {final_output['research_summary']['expert_opinions']}
- **Content Angles Explored**: {final_output['research_summary']['content_angles']}

## SEO Optimizations
- **Technical SEO Checks Passed**: {final_output['optimization_summary']['technical_seo_passed']}/4
- **Internal Links Suggested**: {final_output['optimization_summary']['internal_links_suggested']}
- **External Links Suggested**: {final_output['optimization_summary']['external_links_suggested']}

## Next Steps
1. Review the final blog post in `final_blog_post.md`
2. Check the SEO optimization report for detailed recommendations
3. Implement suggested internal/external links
4. Schedule publication and promotion
5. Monitor performance metrics post-publication

---
*Generated by Blog Team AI on {final_output['creation_date']}*
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(brief)
    
    def get_workflow_status(self, workflow_id: str) -> Dict:
        """
        Get status of a specific workflow
        """
        workflow_dir = os.path.join(self.output_dir, workflow_id)
        if not os.path.exists(workflow_dir):
            return {"error": "Workflow not found"}
        
        # Check which phases are complete
        phases = ["research", "content", "seo"]
        completed_phases = []
        
        for phase in phases:
            phase_file = os.path.join(workflow_dir, f"{phase}_data.json")
            if os.path.exists(phase_file):
                completed_phases.append(phase)
        
        return {
            "workflow_id": workflow_id,
            "completed_phases": completed_phases,
            "total_phases": len(phases),
            "status": "completed" if len(completed_phases) == len(phases) else "in_progress"
        }
    
    def list_workflows(self) -> List[Dict]:
        """
        List all completed workflows
        """
        workflows = []
        
        if not os.path.exists(self.output_dir):
            return workflows
        
        for item in os.listdir(self.output_dir):
            item_path = os.path.join(self.output_dir, item)
            if os.path.isdir(item_path):
                summary_file = os.path.join(item_path, "workflow_summary.json")
                if os.path.exists(summary_file):
                    try:
                        with open(summary_file, 'r', encoding='utf-8') as f:
                            summary = json.load(f)
                            workflows.append({
                                "workflow_id": summary["workflow_id"],
                                "topic": summary["topic"],
                                "creation_date": summary["creation_date"],
                                "seo_score": summary["seo_score"],
                                "word_count": summary["word_count"]
                            })
                    except Exception as e:
                        continue
        
        return sorted(workflows, key=lambda x: x["creation_date"], reverse=True)
    
    def _print_blog_content(self, final_output: Dict) -> None:
        """
        Print the generated blog content to the console
        """
        print("\n" + "="*80)
        print("GENERATED BLOG CONTENT")
        print("="*80)
        print(f"Title: {final_output['final_title']}")
        print(f"Meta Description: {final_output['final_meta_description']}")
        print(f"Word Count: {final_output['word_count']} words")
        print(f"SEO Score: {final_output['seo_score']}%")
        print("-"*80)
        print(final_output['final_content'])
        print("="*80)
    
    def print_workflow_content(self, workflow_id: str) -> None:
        """
        Print content from an existing workflow
        """
        workflow_dir = os.path.join(self.output_dir, workflow_id)
        summary_file = os.path.join(workflow_dir, "workflow_summary.json")
        
        if not os.path.exists(summary_file):
            print(f"Workflow {workflow_id} not found")
            return
        
        try:
            with open(summary_file, 'r', encoding='utf-8') as f:
                summary = json.load(f)
            self._print_blog_content(summary)
        except Exception as e:
            print(f"Error reading workflow: {str(e)}")
    
    def print_latest_workflow(self) -> None:
        """
        Print content from the most recent workflow
        """
        workflows = self.list_workflows()
        if workflows:
            latest = workflows[0]
            self.print_workflow_content(latest['workflow_id'])
        else:
            print("No workflows found")
    
    def _create_blog_page_file(self, workflow_id: str, result: Dict) -> str:
        """Create a standalone HTML blog page"""
        blog_dir = os.path.join(self.output_dir, workflow_id)
        blog_page_path = os.path.join(blog_dir, "blog_page.html")
        
        # Convert markdown content to HTML
        content_html = result['final_content'].replace('\n\n', '</p><p>')
        content_html = content_html.replace('\n', '<br>')
        content_html = content_html.replace('# ', '<h1>').replace('</p><p><h1>', '</p><h1>')
        content_html = content_html.replace('## ', '<h2>').replace('</p><p><h2>', '</p><h2>')
        content_html = content_html.replace('### ', '<h3>').replace('</p><p><h3>', '</p><h3>')
        content_html = content_html.replace('**', '<strong>').replace('**', '</strong>')
        content_html = f"<p>{content_html}</p>"
        
        # Handle headings properly
        content_html = content_html.replace('<p><h1>', '<h1>').replace('</p><p>', '</p>\n<p>')
        content_html = content_html.replace('<p><h2>', '<h2>').replace('<p><h3>', '<h3>')
        
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{result['final_title']}</title>
    <meta name="description" content="{result['final_meta_description']}">
    <meta name="robots" content="index, follow">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{result['final_title']}">
    <meta property="og:description" content="{result['final_meta_description']}">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:title" content="{result['final_title']}">
    <meta property="twitter:description" content="{result['final_meta_description']}">
    
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            background-color: #f8f9fa;
        }}
        
        .article-container {{
            background: white;
            padding: 3rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.5rem;
            margin-bottom: 2rem;
        }}
        
        h2 {{
            color: #34495e;
            margin-top: 2rem;
            margin-bottom: 1rem;
            border-left: 4px solid #3498db;
            padding-left: 1rem;
        }}
        
        h3 {{
            color: #2c3e50;
            margin-top: 1.5rem;
        }}
        
        p {{
            margin-bottom: 1.5rem;
            text-align: justify;
        }}
        
        strong {{
            color: #2c3e50;
            font-weight: 600;
        }}
        
        .meta-info {{
            background: #ecf0f1;
            padding: 1rem;
            border-radius: 4px;
            margin-bottom: 2rem;
            font-size: 0.9rem;
            color: #7f8c8d;
        }}
        
        .meta-info span {{
            margin-right: 2rem;
        }}
        
        .generated-by {{
            text-align: center;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid #ecf0f1;
            color: #95a5a6;
            font-size: 0.8rem;
        }}
        
        @media (max-width: 768px) {{
            body {{
                padding: 1rem;
            }}
            
            .article-container {{
                padding: 1.5rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="article-container">
        <div class="meta-info">
            <span><strong>Word Count:</strong> {result['word_count']} words</span>
            <span><strong>SEO Score:</strong> {result['seo_score']}%</span>
            <span><strong>Target Audience:</strong> {result['target_audience']}</span>
            <span><strong>Created:</strong> {datetime.now().strftime('%B %d, %Y')}</span>
        </div>
        
        {content_html}
        
        <div class="generated-by">
            <p>Generated by AI Blog Writing Team<br>
            Powered by Multi-Agent Content Creation System</p>
        </div>
    </div>
</body>
</html>"""
        
        with open(blog_page_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        return blog_page_path

# Example usage and testing functions
def example_usage():
    """
    Example of how to use the BlogTeamCoordinator
    """
    coordinator = BlogTeamCoordinator()
    
    # Create a blog post about "Digital Marketing"
    result = coordinator.create_blog_post(
        topic="Digital Marketing Strategies",
        target_audience="small business owners",
        tone="conversational",
        word_count=2000,
        custom_keywords=["digital marketing", "online marketing", "marketing strategies"]
    )
    
    print("\n" + "="*50)
    print("WORKFLOW COMPLETED!")
    print("="*50)
    print(f"Final Title: {result['final_title']}")
    print(f"Word Count: {result['word_count']}")
    print(f"SEO Score: {result['seo_score']}%")
    print(f"Files saved to: blog_output/{result['workflow_id']}/")

if __name__ == "__main__":
    # Run example
    example_usage()