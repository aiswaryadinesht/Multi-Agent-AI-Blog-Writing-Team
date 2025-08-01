import streamlit as st
import os
import json
from datetime import datetime
import time
from blog_team_coordinator import BlogTeamCoordinator

# Configure Streamlit page
st.set_page_config(
    page_title="AI Blog Writing Team",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}

.success-box {
    padding: 1rem;
    border-radius: 0.5rem;
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
    margin: 1rem 0;
}

.blog-content {
    background-color: #f8f9fa;
    padding: 2rem;
    border-radius: 0.5rem;
    border: 1px solid #dee2e6;
    margin: 1rem 0;
}

.metrics-container {
    display: flex;
    justify-content: space-around;
    margin: 1rem 0;
}

.workflow-card {
    background-color: white;
    padding: 1.5rem;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin: 1rem 0;
    border-left: 4px solid #1f77b4;
}
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'coordinator' not in st.session_state:
        st.session_state.coordinator = BlogTeamCoordinator()
    if 'current_result' not in st.session_state:
        st.session_state.current_result = None
    if 'blog_created' not in st.session_state:
        st.session_state.blog_created = False

def create_blog_page_file(workflow_id, result):
    """Create a standalone HTML blog page"""
    blog_dir = os.path.join("blog_output", workflow_id)
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
    
    html_template = f"""
    <!DOCTYPE html>
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
    </html>
    """
    
    with open(blog_page_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    return blog_page_path

def main():
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Blog Writing Team</h1>', unsafe_allow_html=True)
    st.markdown("### Create professional, SEO-optimized blog content with AI agents")
    
    # Sidebar for blog creation
    with st.sidebar:
        st.header("📝 Create New Blog")
        
        # Blog creation form
        with st.form("blog_creation_form"):
            topic = st.text_input(
                "Blog Topic", 
                placeholder="e.g., Machine Learning for Beginners",
                help="Enter the main topic for your blog post"
            )
            
            target_audience = st.selectbox(
                "Target Audience",
                ["General readers", "Beginners", "Professionals", "Students", "Developers", 
                 "Business owners", "Marketers", "IT managers", "Healthcare professionals"]
            )
            
            tone = st.selectbox(
                "Writing Tone",
                ["Conversational", "Professional", "Technical", "Casual"],
                help="Choose the tone that best fits your audience"
            )
            
            word_count = st.slider(
                "Target Word Count",
                min_value=800,
                max_value=3000,
                value=1500,
                step=100,
                help="Desired length of the blog post"
            )
            
            # Advanced options
            with st.expander("🔧 Advanced Options"):
                custom_keywords = st.text_input(
                    "Custom Keywords (optional)",
                    placeholder="keyword1, keyword2, keyword3",
                    help="Comma-separated keywords for SEO optimization"
                )
            
            submitted = st.form_submit_button("🚀 Generate Blog", use_container_width=True)
            
            if submitted and topic:
                # Parse custom keywords
                keywords = None
                if custom_keywords:
                    keywords = [kw.strip() for kw in custom_keywords.split(",") if kw.strip()]
                
                # Create progress indicators
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Update progress
                    status_text.text("🔍 Starting research phase...")
                    progress_bar.progress(10)
                    time.sleep(0.5)
                    
                    status_text.text("📊 Gathering trends and data...")
                    progress_bar.progress(30)
                    time.sleep(0.5)
                    
                    status_text.text("✍️ Writing content...")
                    progress_bar.progress(60)
                    time.sleep(0.5)
                    
                    status_text.text("🔧 Optimizing for SEO...")
                    progress_bar.progress(80)
                    
                    # Generate the blog
                    result = st.session_state.coordinator.create_blog_post(
                        topic=topic,
                        target_audience=target_audience.lower(),
                        tone=tone.lower(),
                        word_count=word_count,
                        custom_keywords=keywords
                    )
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Blog created successfully!")
                    
                    # Store result in session state
                    st.session_state.current_result = result
                    st.session_state.blog_created = True
                    
                    # Create blog page file
                    blog_page_path = create_blog_page_file(result['workflow_id'], result)
                    
                    st.success("🎉 Blog generated successfully!")
                    time.sleep(1)
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error generating blog: {str(e)}")
                    progress_bar.empty()
                    status_text.empty()
    
    # Main content area
    if st.session_state.blog_created and st.session_state.current_result:
        result = st.session_state.current_result
        
        # Success message and metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Word Count", f"{result['word_count']}")
        
        with col2:
            st.metric("SEO Score", f"{result['seo_score']}%")
        
        with col3:
            st.metric("Readability", result['readability_score'].title())
        
        with col4:
            st.metric("Performance", result['performance_prediction']['search_ranking_potential'].title())
        
        # Blog content tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📖 Blog Content", "🔗 Blog Page", "📊 Analytics", "📁 Files"])
        
        with tab1:
            st.subheader("Generated Blog Content")
            
            # Title and meta description
            st.markdown(f"**Title:** {result['final_title']}")
            st.markdown(f"**Meta Description:** {result['final_meta_description']}")
            st.markdown("---")
            
            # Blog content
            st.markdown(result['final_content'])
            
            # Download buttons
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "⬇️ Download Markdown",
                    result['final_content'],
                    file_name=f"{result['topic'].replace(' ', '_').lower()}.md",
                    mime="text/markdown"
                )
            
            with col2:
                # Create HTML version for download
                html_content = f"""
                <html>
                <head>
                    <title>{result['final_title']}</title>
                    <meta name="description" content="{result['final_meta_description']}">
                </head>
                <body>
                    {result['final_content'].replace('\n', '<br>')}
                </body>
                </html>
                """
                st.download_button(
                    "⬇️ Download HTML",
                    html_content,
                    file_name=f"{result['topic'].replace(' ', '_').lower()}.html",
                    mime="text/html"
                )
        
        with tab2:
            st.subheader("Standalone Blog Page")
            
            # Generate blog page link
            blog_page_path = os.path.join("blog_output", result['workflow_id'], "blog_page.html")
            
            if os.path.exists(blog_page_path):
                # Get the absolute path for the blog page
                abs_path = os.path.abspath(blog_page_path)
                file_url = f"file:///{abs_path.replace(os.sep, '/')}"
                
                st.success("🎉 Blog page created successfully!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    **📄 Blog Page Details:**
                    - **File Location:** `{blog_page_path}`
                    - **Format:** Standalone HTML
                    - **Features:** SEO optimized, mobile responsive
                    - **Status:** Ready to publish
                    """)
                
                with col2:
                    st.markdown(f"""
                    **🔗 Access Options:**
                    - Open the file directly in your browser
                    - Upload to your web server
                    - Share the HTML file
                    - Embed in your website
                    """)
                
                # Instructions
                st.info(f"""
                **How to access your blog page:**
                1. Navigate to the file: `{abs_path}`
                2. Double-click to open in your default browser
                3. Or copy this path to your browser: `{file_url}`
                """)
                
                # Show preview
                st.subheader("📱 Blog Page Preview")
                
                # Read and display the HTML content in an iframe-like manner
                with open(blog_page_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                st.components.v1.html(html_content, height=600, scrolling=True)
            
            else:
                st.error("Blog page file not found. Try regenerating the blog.")
        
        with tab3:
            st.subheader("📊 Content Analytics")
            
            # SEO Analysis
            st.markdown("**SEO Performance:**")
            seo_score = result['seo_score']
            
            if seo_score >= 80:
                st.success(f"Excellent SEO score: {seo_score}% ✅")
            elif seo_score >= 60:
                st.info(f"Good SEO score: {seo_score}% ℹ️")
            else:
                st.warning(f"SEO score needs improvement: {seo_score}% ⚠️")
            
            # Performance Predictions
            st.markdown("**Performance Predictions:**")
            predictions = result['performance_prediction']
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"🎯 **Search Ranking:** {predictions['search_ranking_potential'].title()}")
                st.write(f"📈 **Traffic Estimate:** {predictions['estimated_organic_traffic']}")
            
            with col2:
                st.write(f"👥 **Engagement:** {predictions['engagement_potential'].title()}")
                st.write(f"📱 **Social Sharing:** {predictions['social_sharing_potential'].title()}")
            
            # Research Summary
            st.markdown("**Research Summary:**")
            research_summary = result['research_summary']
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"📊 **Trends Analyzed:** {research_summary['trends_found']}")
                st.write(f"📈 **Statistics Collected:** {research_summary['statistics_collected']}")
            
            with col2:
                st.write(f"👨‍💼 **Expert Opinions:** {research_summary['expert_opinions']}")
                st.write(f"💡 **Content Angles:** {research_summary['content_angles']}")
        
        with tab4:
            st.subheader("📁 Generated Files")
            
            workflow_dir = os.path.join("blog_output", result['workflow_id'])
            
            if os.path.exists(workflow_dir):
                st.success(f"All files saved to: `{workflow_dir}`")
                
                # List all files
                files = os.listdir(workflow_dir)
                
                for file in files:
                    file_path = os.path.join(workflow_dir, file)
                    file_size = os.path.getsize(file_path)
                    
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"📄 {file}")
                    
                    with col2:
                        st.write(f"{file_size:,} bytes")
                    
                    with col3:
                        if file.endswith(('.md', '.txt', '.json', '.html')):
                            with open(file_path, 'r', encoding='utf-8') as f:
                                file_content = f.read()
                            
                            st.download_button(
                                "⬇️",
                                file_content,
                                file_name=file,
                                key=f"download_{file}"
                            )
    
    # Existing workflows section
    st.header("📚 Existing Blog Posts")
    
    workflows = st.session_state.coordinator.list_workflows()
    
    if workflows:
        st.write(f"Found {len(workflows)} existing blog posts:")
        
        for i, workflow in enumerate(workflows):
            with st.expander(f"📖 {workflow['topic']} (SEO: {workflow['seo_score']}%)"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Word Count:** {workflow['word_count']}")
                    st.write(f"**SEO Score:** {workflow['seo_score']}%")
                
                with col2:
                    created_date = workflow['creation_date'].split('T')[0]
                    st.write(f"**Created:** {created_date}")
                    st.write(f"**ID:** {workflow['workflow_id'][:20]}...")
                
                with col3:
                    if st.button(f"View Content", key=f"view_{i}"):
                        # Load and display this workflow's content
                        workflow_dir = os.path.join("blog_output", workflow['workflow_id'])
                        summary_file = os.path.join(workflow_dir, "workflow_summary.json")
                        
                        if os.path.exists(summary_file):
                            with open(summary_file, 'r', encoding='utf-8') as f:
                                workflow_data = json.load(f)
                            
                            st.session_state.current_result = workflow_data
                            st.session_state.blog_created = True
                            st.rerun()
    else:
        st.info("No existing blog posts found. Create your first blog using the sidebar!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>🤖 Powered by Multi-Agent AI Blog Writing System</p>
        <p>Research Agent • Content Writer Agent • SEO Editor Agent</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()