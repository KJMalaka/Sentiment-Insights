from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from .base import SentimentLayer
from typing import Dict, Any

class VaderLayer(SentimentLayer):
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(self, comment: str) -> Dict[str, Any]:
        scores = self.analyzer.polarity_scores(comment)
        compound = scores['compound']
        
        if compound >= 0.05:
            label = "positive"
        elif compound <= -0.05:
            label = "negative"
        else:
            label = "neutral"
            
        return {
            "label": label,
            "compound_score": compound,
            "scores": scores
        }
