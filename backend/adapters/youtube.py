import re
import os
from typing import Dict, Any
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .base import PlatformAdapter
from fastapi import HTTPException

class YouTubeAdapter(PlatformAdapter):
    def __init__(self):
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key or api_key == "your_youtube_api_key_here":
            raise ValueError("YOUTUBE_API_KEY is missing or not configured in environment variables.")
        self.youtube = build("youtube", "v3", developerKey=api_key)

    def extract_video_id(self, url: str) -> str:
        # Regex to match youtube.com and youtu.be URLs
        regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
        match = re.search(regex, url)
        if match:
            return match.group(1)
        raise ValueError("Invalid YouTube URL. Could not extract video ID.")

    def fetch_video_data(self, video_id: str) -> Dict[str, Any]:
        try:
            # Fetch video details
            video_response = self.youtube.videos().list(
                part="snippet,statistics",
                id=video_id
            ).execute()

            if not video_response.get("items"):
                raise HTTPException(status_code=404, detail="Video not found, private, or deleted.")
            
            video_item = video_response["items"][0]
            snippet = video_item["snippet"]
            statistics = video_item["statistics"]
            channel_id = snippet["channelId"]

            thumbnails = snippet.get("thumbnails", {})
            thumbnail_url = (
                thumbnails.get("maxres", {}).get("url")
                or thumbnails.get("high", {}).get("url")
                or thumbnails.get("medium", {}).get("url")
                or thumbnails.get("default", {}).get("url")
            )

            # Fetch channel details for subscriber count
            channel_response = self.youtube.channels().list(
                part="statistics",
                id=channel_id
            ).execute()
            
            subscriber_count = 0
            if channel_response.get("items"):
                subscriber_count = int(channel_response["items"][0]["statistics"].get("subscriberCount", 0))

            # Fetch comments with pagination (up to 500)
            comments = []
            next_page_token = None
            
            while len(comments) < 500:
                try:
                    comment_response = self.youtube.commentThreads().list(
                        part="snippet",
                        videoId=video_id,
                        maxResults=100,
                        pageToken=next_page_token,
                        textFormat="plainText"
                    ).execute()
                    
                    for item in comment_response.get("items", []):
                        top_level_comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                        comments.append(top_level_comment)
                        if len(comments) >= 500:
                            break
                            
                    next_page_token = comment_response.get("nextPageToken")
                    if not next_page_token:
                        break
                except HttpError as e:
                    if e.resp.status == 403 and "disabled comments" in str(e).lower():
                        # Comments disabled but we still return video data
                        break
                    elif e.resp.status == 403 and "quota" in str(e).lower():
                        raise HTTPException(status_code=429, detail="YouTube API quota exceeded.")
                    else:
                        raise

            return {
                "title": snippet["title"],
                "description": snippet["description"],
                "channel_name": snippet["channelTitle"],
                "thumbnail_url": thumbnail_url,
                "subscriber_count": subscriber_count,
                "view_count": int(statistics.get("viewCount", 0)),
                "like_count": int(statistics.get("likeCount", 0)),
                "publish_date": snippet["publishedAt"],
                "comments": comments
            }

        except HttpError as e:
            if e.resp.status == 403 and "quota" in str(e).lower():
                raise HTTPException(status_code=429, detail="YouTube API quota exceeded.")
            raise HTTPException(status_code=500, detail=f"YouTube API error: {str(e)}")
