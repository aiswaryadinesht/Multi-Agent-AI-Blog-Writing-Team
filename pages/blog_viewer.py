import streamlit as st
import os
import json
from blog_team_coordinator import BlogTeamCoordinator

st.set_page_config(
    page_title="Blog Viewer",
    page_icon="📖",
    layout="wide"
)

def main():
    st.title("📖 Blog Content Viewer")
    st.markdown("View and manage all your generated blog posts")
    
    coordinator = BlogTeamCoordinator()
    workflows = coordinator.list_workflows()
    
    if not workflows:
        st.info("No blog posts found. Create some blogs first!")
        return
    
    # Sidebar for blog selection
    with st.sidebar:
        st.header("📚 Select Blog Post")
        
        selected_blog = st.selectbox(
            "Choose a blog to view:",
            options=range(len(workflows)),
            format_func=lambda x: f"{workflows[x]['topic']} ({workflows[x]['seo_score']}%)"
        )
        
        if st.button("🔄 Refresh List"):
            st.rerun()
    
    # Display selected blog
    if selected_blog is not None:
        workflow = workflows[selected_blog]
        workflow_dir = os.path.join("blog_output", workflow['workflow_id'])
        summary_file = os.path.join(workflow_dir, "workflow_summary.json")
        
        if os.path.exists(summary_file):
            with open(summary_file, 'r', encoding='utf-8') as f:
                blog_data = json.load(f)
            
            # Blog header
            st.header(blog_data['final_title'])
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Word Count", blog_data['word_count'])
            with col2:
                st.metric("SEO Score", f"{blog_data['seo_score']}%")
            with col3:
                st.metric("Readability", blog_data['readability_score'].title())
            with col4:
                created_date = blog_data['creation_date'].split('T')[0]
                st.metric("Created", created_date)
            
            # Meta description
            st.markdown(f"**Meta Description:** {blog_data['final_meta_description']}")
            st.markdown("---")
            
            # Blog content
            st.markdown(blog_data['final_content'])
            
            # Download section
            st.markdown("---")
            st.subheader("📥 Download Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    "⬇️ Download Markdown",
                    blog_data['final_content'],
                    file_name=f"{blog_data['topic'].replace(' ', '_')}.md",
                    mime="text/markdown"
                )
            
            with col2:
                # Create HTML version
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>{blog_data['final_title']}</title>
                    <meta name="description" content="{blog_data['final_meta_description']}">
                </head>
                <body>
                    <h1>{blog_data['final_title']}</h1>
                    {blog_data['final_content'].replace('\n\n', '</p><p>').replace('\n', '<br>')}
                </body>
                </html>
                """
                
                st.download_button(
                    "⬇️ Download HTML",
                    html_content,
                    file_name=f"{blog_data['topic'].replace(' ', '_')}.html",
                    mime="text/html"
                )
            
            with col3:
                # Create blog page link
                blog_page_path = os.path.join(workflow_dir, "blog_page.html")
                if os.path.exists(blog_page_path):
                    st.success("🔗 Blog page available")
                    abs_path = os.path.abspath(blog_page_path)
                    st.caption(f"Open: {abs_path}")
        else:
            st.error("Blog data not found")

if __name__ == "__main__":
    main()