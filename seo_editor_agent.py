import re
from typing import Dict, List, Optional, Tuple
from collections import Counter
import math

class SEOEditorAgent:
    """
    SEO Editor Agent for Blog Writing Team
    Optimizes content for search engines and improves overall quality
    """
    
    def __init__(self):
        self.readability_weights = {
            "sentence_length": 0.3,
            "word_complexity": 0.2,
            "paragraph_length": 0.2,
            "transition_words": 0.3
        }
        self.optimized_content = {}
    
    def optimize_content(self, content_data: Dict, research_data: Dict, 
                        target_keywords: Optional[List[str]] = None) -> Dict:
        """
        Main optimization function that handles all SEO and quality improvements
        """
        print(f"Optimizing content for SEO and readability")
        
        if not target_keywords:
            target_keywords = [kw["keyword"] for kw in research_data.get("keywords", [])]
        
        optimized = {
            "original_content": content_data,
            "seo_optimized_title": self._optimize_title(content_data["title"], target_keywords),
            "optimized_meta_description": self._optimize_meta_description(
                content_data["meta_description"], target_keywords
            ),
            "keyword_optimized_content": self._optimize_keyword_density(
                content_data["full_text"], target_keywords
            ),
            "internal_links": self._suggest_internal_links(content_data["full_text"]),
            "external_links": self._suggest_external_links(research_data),
            "readability_improvements": self._improve_readability(content_data["full_text"]),
            "seo_score": self._calculate_seo_score(content_data, target_keywords),
            "technical_seo": self._check_technical_seo(content_data),
            "performance_predictions": self._predict_performance(content_data, target_keywords),
            "final_content": ""
        }
        
        # Apply all optimizations to create final content
        optimized["final_content"] = self._apply_all_optimizations(content_data, optimized)
        
        self.optimized_content = optimized
        return optimized
    
    def _optimize_title(self, title: str, keywords: List[str]) -> Dict:
        """
        Optimize title for SEO while maintaining readability
        """
        primary_keyword = keywords[0] if keywords else ""
        
        # Check if primary keyword is in title
        keyword_in_title = any(kw.lower() in title.lower() for kw in keywords[:2])
        
        suggestions = []
        if not keyword_in_title and primary_keyword:
            suggestions.append(f"Include primary keyword '{primary_keyword}' in title")
        
        if len(title) > 60:
            suggestions.append(f"Title is {len(title)} characters, consider shortening to under 60")
        elif len(title) < 30:
            suggestions.append(f"Title is {len(title)} characters, consider making it more descriptive")
        
        # Generate optimized version
        optimized_title = title
        if not keyword_in_title and primary_keyword:
            if ":" in title:
                parts = title.split(":", 1)
                optimized_title = f"{parts[0]}: {primary_keyword} {parts[1]}".strip()
            else:
                optimized_title = f"{primary_keyword}: {title}"
        
        return {
            "original": title,
            "optimized": optimized_title,
            "length": len(optimized_title),
            "keyword_present": keyword_in_title,
            "suggestions": suggestions
        }
    
    def _optimize_meta_description(self, meta_desc: str, keywords: List[str]) -> Dict:
        """
        Optimize meta description for click-through rates
        """
        primary_keyword = keywords[0] if keywords else ""
        keyword_present = any(kw.lower() in meta_desc.lower() for kw in keywords[:2])
        
        suggestions = []
        if not keyword_present and primary_keyword:
            suggestions.append(f"Include primary keyword '{primary_keyword}' in meta description")
        
        if len(meta_desc) > 160:
            suggestions.append(f"Meta description is {len(meta_desc)} characters, trim to under 160")
        elif len(meta_desc) < 120:
            suggestions.append("Consider making meta description more descriptive (120-160 chars)")
        
        # Check for action words
        action_words = ["discover", "learn", "find out", "get", "download", "read", "explore"]
        has_action = any(word in meta_desc.lower() for word in action_words)
        if not has_action:
            suggestions.append("Add action words to encourage clicks")
        
        optimized_desc = meta_desc
        if not keyword_present and primary_keyword:
            optimized_desc = f"{primary_keyword}: {meta_desc}"
            if len(optimized_desc) > 160:
                optimized_desc = f"{meta_desc[:140]}... Learn more about {primary_keyword}!"
        
        return {
            "original": meta_desc,
            "optimized": optimized_desc,
            "length": len(optimized_desc),
            "keyword_present": keyword_present,
            "has_action_words": has_action,
            "suggestions": suggestions
        }
    
    def _optimize_keyword_density(self, content: str, keywords: List[str]) -> Dict:
        """
        Analyze and optimize keyword density
        """
        word_count = len(content.split())
        keyword_analysis = {}
        
        for keyword in keywords[:5]:  # Analyze top 5 keywords
            # Count exact matches and variations
            exact_count = len(re.findall(rf'\b{re.escape(keyword.lower())}\b', content.lower()))
            density = (exact_count / word_count) * 100 if word_count > 0 else 0
            
            # Determine if density is optimal (1-3% for primary, 0.5-1% for secondary)
            is_primary = keyword == keywords[0] if keywords else False
            optimal_range = (1, 3) if is_primary else (0.5, 1)
            
            status = "optimal"
            if density < optimal_range[0]:
                status = "under-optimized"
            elif density > optimal_range[1]:
                status = "over-optimized"
            
            keyword_analysis[keyword] = {
                "count": exact_count,
                "density": round(density, 2),
                "status": status,
                "optimal_range": optimal_range
            }
        
        return {
            "total_words": word_count,
            "keyword_analysis": keyword_analysis,
            "suggestions": self._generate_keyword_suggestions(keyword_analysis)
        }
    
    def _generate_keyword_suggestions(self, analysis: Dict) -> List[str]:
        """
        Generate keyword optimization suggestions
        """
        suggestions = []
        for keyword, data in analysis.items():
            if data["status"] == "under-optimized":
                suggestions.append(f"Increase '{keyword}' usage - currently {data['density']}%, target {data['optimal_range'][0]}-{data['optimal_range'][1]}%")
            elif data["status"] == "over-optimized":
                suggestions.append(f"Reduce '{keyword}' usage - currently {data['density']}%, target {data['optimal_range'][0]}-{data['optimal_range'][1]}%")
        
        return suggestions
    
    def _suggest_internal_links(self, content: str) -> List[Dict]:
        """
        Suggest internal linking opportunities
        """
        # Extract topics and suggest related internal links
        internal_links = [
            {
                "anchor_text": "comprehensive guide",
                "suggested_link": "/related-topic-guide",
                "position": "introduction",
                "reason": "Provides additional value to readers"
            },
            {
                "anchor_text": "best practices",
                "suggested_link": "/best-practices-article",
                "position": "main content",
                "reason": "Supports the main topic with detailed information"
            },
            {
                "anchor_text": "case studies",
                "suggested_link": "/case-studies",
                "position": "conclusion",
                "reason": "Offers proof of concept and real examples"
            }
        ]
        
        return internal_links
    
    def _suggest_external_links(self, research_data: Dict) -> List[Dict]:
        """
        Suggest high-quality external links to boost authority
        """
        external_links = []
        
        # Link to statistics sources
        for stat in research_data.get("statistics", []):
            external_links.append({
                "anchor_text": stat["stat"][:50] + "...",
                "suggested_link": f"https://source-link.com",
                "source": stat["source"],
                "purpose": "Citation for credibility"
            })
        
        # Link to expert sources
        for expert in research_data.get("expert_opinions", []):
            external_links.append({
                "anchor_text": f"{expert['expert']}, {expert['title']}",
                "suggested_link": f"https://expert-profile.com",
                "source": "Expert Profile",
                "purpose": "Authority and credibility"
            })
        
        return external_links[:5]  # Limit to 5 suggestions
    
    def _improve_readability(self, content: str) -> Dict:
        """
        Analyze and improve content readability
        """
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        paragraphs = content.split('\n\n')
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        words = content.split()
        
        # Calculate readability metrics
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        avg_paragraph_length = sum(len(p.split()) for p in paragraphs) / len(paragraphs) if paragraphs else 0
        
        # Count transition words
        transition_words = [
            "however", "therefore", "furthermore", "moreover", "additionally",
            "consequently", "meanwhile", "nevertheless", "specifically", "for example",
            "in addition", "as a result", "on the other hand", "in contrast"
        ]
        transition_count = sum(1 for word in words if word.lower().rstrip('.,!?') in transition_words)
        transition_ratio = (transition_count / len(words)) * 100 if words else 0
        
        # Generate readability score (simplified Flesch-like scoring)
        readability_score = self._calculate_readability_score(
            avg_sentence_length, avg_paragraph_length, transition_ratio
        )
        
        suggestions = []
        if avg_sentence_length > 20:
            suggestions.append("Break down long sentences for better readability")
        if avg_paragraph_length > 150:
            suggestions.append("Shorten paragraphs - aim for 100-150 words per paragraph")
        if transition_ratio < 1:
            suggestions.append("Add more transition words to improve flow")
        
        return {
            "readability_score": readability_score,
            "avg_sentence_length": round(avg_sentence_length, 1),
            "avg_paragraph_length": round(avg_paragraph_length, 1),
            "transition_word_ratio": round(transition_ratio, 2),
            "suggestions": suggestions
        }
    
    def _calculate_readability_score(self, sentence_len: float, para_len: float, 
                                   transition_ratio: float) -> str:
        """
        Calculate overall readability score
        """
        # Simplified scoring system
        score = 100
        
        # Penalize long sentences
        if sentence_len > 20:
            score -= (sentence_len - 20) * 2
        
        # Penalize long paragraphs
        if para_len > 150:
            score -= (para_len - 150) * 0.5
        
        # Reward transition words
        if transition_ratio > 1:
            score += min(transition_ratio * 5, 20)
        
        if score >= 80:
            return "excellent"
        elif score >= 60:
            return "good"
        elif score >= 40:
            return "fair"
        else:
            return "needs improvement"
    
    def _calculate_seo_score(self, content_data: Dict, keywords: List[str]) -> Dict:
        """
        Calculate overall SEO score
        """
        score_components = {
            "title_optimization": 0,
            "meta_description": 0,
            "keyword_usage": 0,
            "content_length": 0,
            "headings_structure": 0
        }
        
        # Title optimization (0-25 points)
        title = content_data.get("title", "")
        if any(kw.lower() in title.lower() for kw in keywords[:2]):
            score_components["title_optimization"] = 25
        elif any(kw.lower() in title.lower() for kw in keywords):
            score_components["title_optimization"] = 15
        
        # Meta description (0-20 points)
        meta = content_data.get("meta_description", "")
        if 120 <= len(meta) <= 160 and any(kw.lower() in meta.lower() for kw in keywords):
            score_components["meta_description"] = 20
        elif any(kw.lower() in meta.lower() for kw in keywords):
            score_components["meta_description"] = 10
        
        # Content length (0-20 points)
        word_count = content_data.get("word_count", 0)
        if 1500 <= word_count <= 3000:
            score_components["content_length"] = 20
        elif 1000 <= word_count < 1500:
            score_components["content_length"] = 15
        elif word_count >= 3000:
            score_components["content_length"] = 10
        
        # Keyword usage (0-25 points)
        content = content_data.get("full_text", "")
        primary_keyword = keywords[0] if keywords else ""
        if primary_keyword:
            keyword_count = len(re.findall(rf'\b{re.escape(primary_keyword.lower())}\b', content.lower()))
            density = (keyword_count / word_count) * 100 if word_count > 0 else 0
            if 1 <= density <= 3:
                score_components["keyword_usage"] = 25
            elif 0.5 <= density < 1 or 3 < density <= 4:
                score_components["keyword_usage"] = 15
        
        # Headings structure (0-10 points)
        if content.count("##") >= 3:  # At least 3 H2 headings
            score_components["headings_structure"] = 10
        elif content.count("##") >= 1:
            score_components["headings_structure"] = 5
        
        total_score = sum(score_components.values())
        
        return {
            "total_score": total_score,
            "max_score": 100,
            "percentage": round((total_score / 100) * 100, 1),
            "components": score_components,
            "grade": self._get_seo_grade(total_score)
        }
    
    def _get_seo_grade(self, score: int) -> str:
        """
        Convert SEO score to letter grade
        """
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    def _check_technical_seo(self, content_data: Dict) -> Dict:
        """
        Check technical SEO elements
        """
        checks = {
            "title_length": {
                "status": "pass" if 30 <= len(content_data.get("title", "")) <= 60 else "fail",
                "value": len(content_data.get("title", ""))
            },
            "meta_description_length": {
                "status": "pass" if 120 <= len(content_data.get("meta_description", "")) <= 160 else "fail",
                "value": len(content_data.get("meta_description", ""))
            },
            "content_length": {
                "status": "pass" if content_data.get("word_count", 0) >= 1000 else "fail",
                "value": content_data.get("word_count", 0)
            },
            "heading_structure": {
                "status": "pass" if content_data.get("full_text", "").count("##") >= 2 else "fail",
                "value": content_data.get("full_text", "").count("##")
            }
        }
        
        passed = sum(1 for check in checks.values() if check["status"] == "pass")
        total = len(checks)
        
        return {
            "checks": checks,
            "passed": passed,
            "total": total,
            "score": f"{passed}/{total}"
        }
    
    def _predict_performance(self, content_data: Dict, keywords: List[str]) -> Dict:
        """
        Predict content performance based on optimization factors
        """
        # Simplified performance prediction
        seo_score = self._calculate_seo_score(content_data, keywords)["percentage"]
        
        predictions = {
            "search_ranking_potential": "high" if seo_score >= 80 else "medium" if seo_score >= 60 else "low",
            "estimated_organic_traffic": "1000-5000 visits/month" if seo_score >= 80 else "500-1000 visits/month" if seo_score >= 60 else "100-500 visits/month",
            "engagement_potential": "high" if content_data.get("word_count", 0) >= 1500 else "medium",
            "social_sharing_potential": "high" if "how to" in content_data.get("title", "").lower() or "guide" in content_data.get("title", "").lower() else "medium"
        }
        
        return predictions
    
    def _apply_all_optimizations(self, original_content: Dict, optimizations: Dict) -> str:
        """
        Apply all optimizations to create the final optimized content
        """
        # Start with the original content structure
        optimized_text = original_content["full_text"]
        
        # Apply keyword optimizations (placeholder for actual implementation)
        # In a real implementation, this would carefully insert keywords
        # while maintaining natural flow
        
        # Apply readability improvements
        readability = optimizations["readability_improvements"]
        if "Break down long sentences" in str(readability.get("suggestions", [])):
            # This would contain actual sentence restructuring logic
            pass
        
        return optimized_text
    
    def generate_optimization_report(self) -> str:
        """
        Generate a comprehensive optimization report
        """
        if not self.optimized_content:
            return "No optimization data available"
        
        seo_score = self.optimized_content["seo_score"]
        technical = self.optimized_content["technical_seo"]
        
        report = f"""
SEO Optimization Report
======================

Overall SEO Score: {seo_score['percentage']}% (Grade: {seo_score['grade']})

Technical SEO: {technical['passed']}/{technical['total']} checks passed

Key Improvements Made:
- Title optimization: {self.optimized_content['seo_optimized_title']['suggestions'][:1]}
- Meta description: {self.optimized_content['optimized_meta_description']['suggestions'][:1]}
- Keyword density: {len(self.optimized_content['keyword_optimized_content']['suggestions'])} optimizations
- Internal links: {len(self.optimized_content['internal_links'])} suggestions
- Readability: {self.optimized_content['readability_improvements']['readability_score']} score

Performance Predictions:
- Search ranking potential: {self.optimized_content['performance_predictions']['search_ranking_potential']}
- Estimated traffic: {self.optimized_content['performance_predictions']['estimated_organic_traffic']}
        """
        
        return report.strip()
    
    def export_optimized_content(self, filepath: str) -> None:
        """
        Export the final optimized content
        """
        if not self.optimized_content:
            print("No optimized content to export")
            return
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.optimized_content["final_content"])
        
        # Also export the optimization report
        report_path = filepath.replace('.md', '_optimization_report.txt')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_optimization_report())
        
        print(f"Optimized content exported to {filepath}")
        print(f"Optimization report exported to {report_path}")