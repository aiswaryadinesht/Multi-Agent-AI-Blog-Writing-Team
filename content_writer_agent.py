from typing import Dict, List, Optional
import re
from datetime import datetime

class ContentWriterAgent:
    """
    Content Writer Agent for Blog Writing Team
    Transforms research into engaging, well-structured blog content
    """
    
    def __init__(self):
        self.tone_styles = {
            "professional": {"formality": "high", "personality": "authoritative"},
            "conversational": {"formality": "medium", "personality": "friendly"},
            "casual": {"formality": "low", "personality": "approachable"},
            "technical": {"formality": "high", "personality": "expert"}
        }
        self.content_data = {}
    
    def write_blog_post(self, research_data: Dict, tone: str = "conversational", 
                       word_count_target: int = 1500) -> Dict:
        """
        Main function to create a complete blog post from research data
        """
        print(f"Writing blog post: {research_data['topic']}")
        
        content = {
            "title": self._create_headline(research_data),
            "meta_description": self._create_meta_description(research_data),
            "introduction": self._write_introduction(research_data, tone),
            "main_content": self._structure_main_content(research_data, tone, word_count_target),
            "conclusion": self._write_conclusion(research_data, tone),
            "word_count": 0,
            "readability_score": "medium",
            "tone": tone,
            "timestamp": datetime.now().isoformat()
        }
        
        full_text = self._assemble_full_post(content)
        content["full_text"] = full_text
        content["word_count"] = len(full_text.split())
        
        self.content_data = content
        return content
    
    def _create_headline(self, research_data: Dict) -> str:
        """
        Generate compelling headlines based on research
        """
        topic = research_data["topic"]
        angles = research_data.get("content_angles", [])
        
        if angles:
            primary_angle = angles[0]["angle"]
            if "guide" in primary_angle.lower():
                return f"The Complete {topic} Guide: Everything You Need to Know in 2024"
            elif "mistake" in primary_angle.lower():
                return f"7 Critical {topic} Mistakes That Could Cost You (And How to Fix Them)"
            elif "future" in primary_angle.lower():
                return f"The Future of {topic}: 5 Game-Changing Trends You Can't Ignore"
        
        return f"Master {topic}: A Comprehensive Guide for Success"
    
    def _create_meta_description(self, research_data: Dict) -> str:
        """
        Create SEO-optimized meta description
        """
        topic = research_data["topic"]
        primary_keyword = research_data.get("keywords", [{}])[0].get("keyword", topic.lower())
        
        return f"Discover everything about {primary_keyword} in this comprehensive guide. Learn best practices, avoid common mistakes, and stay ahead of trends. Read more!"
    
    def _write_introduction(self, research_data: Dict, tone: str) -> str:
        """
        Craft engaging introduction that hooks readers
        """
        topic = research_data["topic"]
        pain_points = research_data.get("pain_points", [])
        statistics = research_data.get("statistics", [])
        
        hook = ""
        if statistics:
            stat = statistics[0]["stat"]
            hook = f"Did you know that {stat.lower()}? "
        elif pain_points:
            main_pain = pain_points[0]["pain_point"]
            hook = f"Struggling with {main_pain.lower()}? You're not alone. "
        else:
            hook = f"In today's fast-paced world, {topic.lower()} has become more important than ever. "
        
        if tone == "conversational":
            intro = f"""{hook}

Whether you're just getting started or looking to level up your {topic.lower()} game, this guide has got you covered. We'll walk through everything you need to know, from the basics to advanced strategies that actually work.

By the end of this post, you'll have a clear roadmap for success and the confidence to tackle any {topic.lower()}-related challenge that comes your way."""
        
        elif tone == "professional":
            intro = f"""{hook}

This comprehensive analysis examines the current state of {topic.lower()}, providing evidence-based insights and actionable strategies for organizations and professionals.

Our research-backed approach will equip you with the knowledge and tools necessary to implement effective {topic.lower()} solutions and achieve measurable results."""
        
        else:  # casual or technical
            intro = f"""{hook}

Let's dive into {topic.lower()} and explore what makes it tick. This guide breaks down complex concepts into digestible insights you can actually use.

Ready to become a {topic.lower()} pro? Let's get started."""
        
        return intro
    
    def _structure_main_content(self, research_data: Dict, tone: str, 
                              target_words: int) -> List[Dict]:
        """
        Create structured main content with headings and sections
        """
        topic = research_data["topic"]
        angles = research_data.get("content_angles", [])
        trends = research_data.get("trends", [])
        expert_opinions = research_data.get("expert_opinions", [])
        pain_points = research_data.get("pain_points", [])
        
        sections = []
        
        # Section 1: Understanding the Basics
        sections.append({
            "heading": f"Understanding {topic}: The Fundamentals",
            "content": self._write_fundamentals_section(research_data, tone),
            "type": "educational"
        })
        
        # Section 2: Current Trends and Developments
        if trends:
            sections.append({
                "heading": f"Current Trends Shaping {topic}",
                "content": self._write_trends_section(trends, tone),
                "type": "informational"
            })
        
        # Section 3: Common Challenges and Solutions
        if pain_points:
            sections.append({
                "heading": "Common Challenges and How to Overcome Them",
                "content": self._write_challenges_section(pain_points, tone),
                "type": "problem-solving"
            })
        
        # Section 4: Best Practices and Strategies
        sections.append({
            "heading": f"Best Practices for {topic} Success",
            "content": self._write_best_practices_section(research_data, tone),
            "type": "actionable"
        })
        
        # Section 5: Expert Insights
        if expert_opinions:
            sections.append({
                "heading": "What the Experts Say",
                "content": self._write_expert_section(expert_opinions, tone),
                "type": "authoritative"
            })
        
        return sections
    
    def _write_fundamentals_section(self, research_data: Dict, tone: str) -> str:
        """
        Write the fundamentals section
        """
        topic = research_data["topic"]
        
        if tone == "conversational":
            return f"""Before we dive into the advanced stuff, let's make sure we're all on the same page about what {topic.lower()} actually means.

At its core, {topic.lower()} is about creating solutions that work for real people in real situations. It's not just about following best practices – it's about understanding the why behind those practices.

Here's what you need to know:

• **Definition**: {topic} encompasses the strategies, tools, and methodologies used to achieve specific outcomes
• **Key Components**: Planning, execution, measurement, and optimization
• **Success Factors**: Clear goals, proper resources, and consistent implementation

Think of {topic.lower()} as building a house. You need a solid foundation (understanding), good materials (tools and strategies), and skilled execution (implementation)."""

        return f"""{topic} represents a systematic approach to achieving desired outcomes through strategic planning and execution.

The fundamental principles include:

1. **Strategic Planning**: Establishing clear objectives and methodologies
2. **Resource Allocation**: Optimizing available resources for maximum impact  
3. **Performance Measurement**: Implementing metrics to track progress and success
4. **Continuous Improvement**: Iterating based on data and feedback

Understanding these core concepts is essential for successful {topic.lower()} implementation."""
    
    def _write_trends_section(self, trends: List[Dict], tone: str) -> str:
        """
        Write the trends section
        """
        content = "The landscape is constantly evolving. Here are the key trends you should know about:\n\n"
        
        for i, trend in enumerate(trends[:3], 1):
            content += f"**{i}. {trend['trend']}**\n"
            content += f"This trend is gaining traction because it addresses real market needs and offers tangible benefits. "
            content += f"Organizations that adapt early are seeing significant advantages.\n\n"
        
        return content
    
    def _write_challenges_section(self, pain_points: List[Dict], tone: str) -> str:
        """
        Write the challenges and solutions section
        """
        content = "Let's be honest – there are real challenges you'll face. Here's how to tackle them:\n\n"
        
        for i, pain in enumerate(pain_points[:3], 1):
            content += f"**Challenge {i}: {pain['pain_point']}**\n"
            content += f"*Solution*: Start with small, manageable steps. Focus on building competency gradually rather than trying to solve everything at once. "
            content += f"Consider getting expert guidance or training for your team.\n\n"
        
        return content
    
    def _write_best_practices_section(self, research_data: Dict, tone: str) -> str:
        """
        Write best practices section
        """
        topic = research_data["topic"]
        
        return f"""Here are the proven strategies that consistently deliver results:

**1. Start with Clear Goals**
Define exactly what success looks like for your {topic.lower()} initiative. Vague goals lead to vague results.

**2. Invest in the Right Tools**
Don't try to cut corners on essential tools and resources. The right investment upfront saves time and money later.

**3. Focus on User Experience**
Always keep your end users in mind. What works in theory doesn't always work in practice.

**4. Measure and Adjust**
Set up proper tracking from day one. You can't improve what you don't measure.

**5. Build a Strong Team**
Success in {topic.lower()} is rarely a solo effort. Invest in building capabilities across your team."""
    
    def _write_expert_section(self, expert_opinions: List[Dict], tone: str) -> str:
        """
        Write expert insights section
        """
        content = "Industry leaders share their insights:\n\n"
        
        for expert in expert_opinions[:2]:
            content += f'**{expert["expert"]}, {expert["title"]}**\n'
            content += f'"{expert["quote"]}"\n\n'
            content += "This perspective highlights the importance of staying ahead of industry developments and maintaining a strategic mindset.\n\n"
        
        return content
    
    def _write_conclusion(self, research_data: Dict, tone: str) -> str:
        """
        Write compelling conclusion with call-to-action
        """
        topic = research_data["topic"]
        
        if tone == "conversational":
            return f"""## Ready to Take Action?

We've covered a lot of ground in this guide – from the fundamentals of {topic.lower()} to advanced strategies that actually work in the real world.

The key takeaway? Success in {topic.lower()} isn't about perfection; it's about consistent progress and smart decision-making.

**Your Next Steps:**
1. Pick one strategy from this guide and implement it this week
2. Set up proper tracking to measure your progress
3. Build on your wins and learn from what doesn't work

Remember, every expert was once a beginner. The difference is they took action and kept learning.

What's your first move going to be? Let us know in the comments below – we'd love to hear about your {topic.lower()} journey!"""
        
        return f"""## Conclusion

Effective {topic.lower()} implementation requires strategic thinking, proper resource allocation, and consistent execution. The frameworks and strategies outlined in this guide provide a solid foundation for success.

Organizations that prioritize {topic.lower()} and invest in proper implementation see measurable improvements in their key performance indicators.

**Key Recommendations:**
- Begin with a comprehensive assessment of current capabilities
- Develop a phased implementation plan
- Invest in team training and development
- Establish robust measurement and optimization processes

The path to {topic.lower()} excellence is well-defined. Success depends on commitment to the process and willingness to adapt based on results."""
    
    def _assemble_full_post(self, content: Dict) -> str:
        """
        Assemble the complete blog post
        """
        full_post = f"# {content['title']}\n\n"
        full_post += content['introduction'] + "\n\n"
        
        for section in content['main_content']:
            full_post += f"## {section['heading']}\n\n"
            full_post += section['content'] + "\n\n"
        
        full_post += content['conclusion']
        
        return full_post
    
    def get_content_summary(self) -> str:
        """
        Generate a summary of the written content
        """
        if not self.content_data:
            return "No content available"
        
        return f"""
Content Summary:
Title: {self.content_data['title']}
Word Count: {self.content_data['word_count']} words
Tone: {self.content_data['tone']}
Sections: {len(self.content_data['main_content'])}
Readability: {self.content_data['readability_score']}
        """.strip()
    
    def export_content(self, filepath: str) -> None:
        """
        Export content to markdown file
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.content_data['full_text'])
        print(f"Content exported to {filepath}")