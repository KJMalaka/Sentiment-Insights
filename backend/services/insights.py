from typing import Dict, Any, List
from collections import Counter

def generate_summary(title: str, description: str) -> str:
    # A simple natural language summary without an LLM to avoid latency,
    # or we can use a basic template since we shouldn't fabricate content.
    clean_desc = description.split('\n')[0][:200]
    return f"This video, titled '{title}', is about: {clean_desc}..."

def compute_insights(video_data: Dict[str, Any], analyzed_comments: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_comments = len(analyzed_comments)
    if total_comments == 0:
        return _empty_insights()

    # 1. Compute overall sentiment distribution per layer
    vader_dist = {"positive": 0, "negative": 0, "neutral": 0}
    sklearn_dist = {"positive": 0, "negative": 0, "neutral": 0}
    groq_dist = {"positive": 0, "negative": 0, "neutral": 0}
    
    agreement_count = 0
    controversy_count = 0
    all_themes = []
    nuanced_examples = []
    
    for c in analyzed_comments:
        vader_label = c["vader"]["label"]
        sklearn_label = c["sklearn"]["label"]
        groq_label = c["groq"]["label"]
        
        vader_dist[vader_label] += 1
        sklearn_dist[sklearn_label] += 1
        groq_dist[groq_label] += 1
        
        # Agreement
        if vader_label == sklearn_label == groq_label:
            agreement_count += 1
            
        # Themes and controversy from Groq
        groq_data = c["groq"]
        all_themes.extend(groq_data.get("themes", []))
        
        is_controversial = groq_data.get("is_sarcastic") or groq_data.get("is_mixed")
        if is_controversial:
            controversy_count += 1
            if len(nuanced_examples) < 3:
                nuanced_examples.append(c["text"])
                
    # Normalize distributions to percentages
    for dist in [vader_dist, sklearn_dist, groq_dist]:
        for k in dist:
            dist[k] = round((dist[k] / total_comments) * 100, 1)
            
    agreement_rate = round((agreement_count / total_comments) * 100, 1)
    
    # Top 5 recurring themes
    theme_counts = Counter(all_themes).most_common(5)
    top_themes = [{"theme": t, "count": c} for t, c in theme_counts]
    
    # --- Ambassador Fit Scoring ---
    # Formula: 
    # Positive sentiment ratio (weighted 50%) - we use the average positive across 3 layers
    avg_positive = (vader_dist["positive"] + sklearn_dist["positive"] + groq_dist["positive"]) / 3.0
    score_positive = avg_positive # 0-100 scale
    
    # Engagement rate (comments divided by views, weighted 25%)
    # Let's cap engagement score at some reasonable view/comment ratio.
    # E.g., 5% comment rate is phenomenal (100 score)
    views = max(video_data.get("view_count", 0), 1)
    actual_comments = video_data.get("comments_count", total_comments) 
    # YouTube API gives exact commentCount, but we might just use the fetched list length if it's not provided.
    # Actually, we didn't fetch commentCount, but let's use what we have. 
    # Wait, the adapter didn't return commentCount from statistics. Let's assume actual_comments = len(comments).
    # Wait, engagement on youtube: 0.5% is average. Let's map 1% engagement to 100 score.
    engagement_rate = (total_comments / views) if views > 0 else 0
    score_engagement = min((engagement_rate / 0.01) * 100, 100)
    
    # Inverse of controversy flag frequency (weighted 25%)
    controversy_rate = controversy_count / total_comments
    score_controversy = (1.0 - controversy_rate) * 100
    
    final_score = round(
        (score_positive * 0.5) + 
        (score_engagement * 0.25) + 
        (score_controversy * 0.25)
    )
    
    if final_score >= 75:
        band = "Strong Fit"
    elif final_score >= 50:
        band = "Moderate Fit"
    elif final_score >= 25:
        band = "Weak Fit"
    else:
        band = "Not Recommended"
        
    rationale = f"This video achieves a {band} score of {final_score}/100. "
    rationale += f"The sentiment is on average {avg_positive:.1f}% positive across all analysis layers. "
    rationale += f"Engagement rate contributed a score of {score_engagement:.1f}/100. "
    rationale += f"The content has a controversy/nuance rate of {controversy_rate*100:.1f}%, which is reflected in the inverse controversy score of {score_controversy:.1f}/100."
    if top_themes:
        rationale += f" Key themes driving these conversations include {', '.join([t['theme'] for t in top_themes])}."

    return {
        "summary": generate_summary(video_data["title"], video_data["description"]),
        "distributions": {
            "vader": vader_dist,
            "sklearn": sklearn_dist,
            "groq": groq_dist
        },
        "agreement_rate": agreement_rate,
        "top_themes": top_themes,
        "nuanced_examples": nuanced_examples,
        "ambassador_score": {
            "score": final_score,
            "band": band,
            "rationale": rationale
        }
    }

def _empty_insights() -> Dict[str, Any]:
    return {
        "summary": "No data",
        "distributions": {
            "vader": {"positive": 0, "negative": 0, "neutral": 0},
            "sklearn": {"positive": 0, "negative": 0, "neutral": 0},
            "groq": {"positive": 0, "negative": 0, "neutral": 0}
        },
        "agreement_rate": 0,
        "top_themes": [],
        "nuanced_examples": [],
        "ambassador_score": {
            "score": 0,
            "band": "Not Recommended",
            "rationale": "No comments available to score."
        }
    }
