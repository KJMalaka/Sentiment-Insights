from typing import Dict, Any
from .base import PlatformAdapter
from fastapi import HTTPException

class TikTokAdapter(PlatformAdapter):
    def extract_video_id(self, url: str) -> str:
        return "unsupported"

    def fetch_video_data(self, video_id: str) -> Dict[str, Any]:
        raise HTTPException(
            status_code=501, 
            detail="TikTok is not yet supported. Coming soon, pending API access."
        )
