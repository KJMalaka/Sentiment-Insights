import os
import joblib
from .base import SentimentLayer
from typing import Dict, Any, List
import warnings

# Suppress sklearn warnings if model was trained with different version
warnings.filterwarnings("ignore", category=UserWarning)

class SklearnLayer(SentimentLayer):
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), "sentiment_model.joblib")
        self.pipeline = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            self.pipeline = joblib.load(self.model_path)
        else:
            print(f"Warning: Model not found at {self.model_path}. Run train_sklearn_model.py first.")
            self.pipeline = None

    def analyze(self, comment: str) -> Dict[str, Any]:
        if not self.pipeline:
            return {"label": "neutral", "error": "Model not loaded"}
        
        prediction = self.pipeline.predict([comment])[0]
        # Assuming 1 is positive and 0 is negative from IMDB dataset
        label = "positive" if prediction == 1 else "negative"
        
        # Scikit-learn LogisticRegression doesn't predict "neutral" easily without 
        # thresholding probabilities, so we'll just use probabilities
        probs = self.pipeline.predict_proba([comment])[0]
        
        # If model is very unsure (prob around 0.5), we can classify as neutral
        if 0.4 < probs[1] < 0.6:
            label = "neutral"
            
        return {
            "label": label,
            "confidence": float(max(probs))
        }

    def analyze_batch(self, comments: List[str]) -> List[Dict[str, Any]]:
        if not self.pipeline or not comments:
            return [{"label": "neutral", "error": "Model not loaded"}] * len(comments)
            
        predictions = self.pipeline.predict(comments)
        probs = self.pipeline.predict_proba(comments)
        
        results = []
        for i in range(len(comments)):
            pred = predictions[i]
            prob = probs[i]
            
            label = "positive" if pred == 1 else "negative"
            if 0.4 < prob[1] < 0.6:
                label = "neutral"
                
            results.append({
                "label": label,
                "confidence": float(max(prob))
            })
            
        return results
