from abc import ABC, abstractmethod
from typing import Dict, Any, List

class PlatformAdapter(ABC):
    @abstractmethod
    def extract_video_id(self, url: str) -> str:
        pass

    @abstractmethod
    def fetch_video_data(self, video_id: str) -> Dict[str, Any]:
        """
        Returns a dictionary containing:
        - title: str
        - description: str
        - channel_name: str
        - thumbnail_url: str
        - subscriber_count: int
        - view_count: int
        - like_count: int
        - publish_date: str
        - comments: List[str]
        """
        pass
