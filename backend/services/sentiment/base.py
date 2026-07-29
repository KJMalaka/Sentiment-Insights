from abc import ABC, abstractmethod
from typing import Dict, Any, List

class SentimentLayer(ABC):
    @abstractmethod
    def analyze(self, comment: str) -> Dict[str, Any]:
        """
        Returns a dict with at least:
        - label: str (positive/negative/neutral)
        May contain other layer-specific fields.
        """
        pass
    
    def analyze_batch(self, comments: List[str]) -> List[Dict[str, Any]]:
        return [self.analyze(c) for c in comments]
