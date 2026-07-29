from .base import PlatformAdapter
from .youtube import YouTubeAdapter
from .tiktok import TikTokAdapter
from .instagram import InstagramAdapter

def get_adapter(url: str) -> PlatformAdapter:
    if "youtube.com" in url or "youtu.be" in url or "m.youtube.com" in url:
        return YouTubeAdapter()
    elif "tiktok.com" in url:
        return TikTokAdapter()
    elif "instagram.com" in url:
        return InstagramAdapter()
    else:
        raise ValueError("Unsupported platform or invalid URL")
