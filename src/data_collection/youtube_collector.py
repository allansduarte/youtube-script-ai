"""
YouTube data collection system.

This module handles the collection of YouTube video data including
metadata, performance metrics, and content analysis.
"""

import os
import time
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import yaml


class YouTubeCollector:
    """Collects data from YouTube using the official API."""
    
    def __init__(self, api_key: Optional[str] = None, config_path: str = "config.yaml"):
        """Initialize the YouTube collector."""
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("YouTube API key is required")
        
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self.logger.warning(f"Config file {config_path} not found, using defaults")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "youtube": {
                "max_results": 50,
                "quality_threshold": 0.7
            },
            "data_collection": {
                "min_views": 10000,
                "min_engagement_rate": 0.02,
                "max_duration_minutes": 30,
                "languages": ["pt", "en"],
                "niches": ["tecnologia", "educacao", "entretenimento", "lifestyle", "negocios"]
            }
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the collector."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def search_videos(self, 
                     query: str,
                     max_results: int = 50,
                     published_after: Optional[datetime] = None,
                     order: str = "relevance") -> List[Dict[str, Any]]:
        """Search for videos based on query."""
        try:
            # Set default published_after to 1 year ago if not provided
            if published_after is None:
                published_after = datetime.now() - timedelta(days=365)
            
            search_params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "order": order,
                "maxResults": min(max_results, 50),  # API limit
                "publishedAfter": published_after.isoformat() + "Z",
                "relevanceLanguage": "pt"  # Prioritize Portuguese content
            }
            
            response = self.youtube.search().list(**search_params).execute()
            
            videos = []
            for item in response["items"]:
                video_data = {
                    "video_id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "channel_id": item["snippet"]["channelId"],
                    "channel_title": item["snippet"]["channelTitle"],
                    "published_at": item["snippet"]["publishedAt"],
                    "thumbnails": item["snippet"]["thumbnails"]
                }
                videos.append(video_data)
            
            self.logger.info(f"Found {len(videos)} videos for query: {query}")
            return videos
            
        except HttpError as e:
            self.logger.error(f"HTTP error occurred: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Error searching videos: {e}")
            return []
    
    def get_video_details(self, video_ids: List[str]) -> List[Dict[str, Any]]:
        """Get detailed information for multiple videos."""
        all_details = []
        
        # Process in batches of 50 (API limit)
        for i in range(0, len(video_ids), 50):
            batch_ids = video_ids[i:i+50]
            batch_details = self._get_video_batch_details(batch_ids)
            all_details.extend(batch_details)
            
            # Rate limiting
            time.sleep(0.1)
        
        return all_details
    
    def _get_video_batch_details(self, video_ids: List[str]) -> List[Dict[str, Any]]:
        """Get detailed information for a batch of videos."""
        try:
            video_params = {
                "part": "snippet,statistics,contentDetails,status",
                "id": ",".join(video_ids)
            }
            
            response = self.youtube.videos().list(**video_params).execute()
            
            videos = []
            for item in response["items"]:
                # Parse duration
                duration = self._parse_duration(item["contentDetails"]["duration"])
                
                # Calculate engagement rate
                stats = item["statistics"]
                views = int(stats.get("viewCount", 0))
                likes = int(stats.get("likeCount", 0))
                comments = int(stats.get("commentCount", 0))
                
                engagement_rate = (likes + comments) / max(views, 1) if views > 0 else 0
                
                video_data = {
                    "video_id": item["id"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "channel_id": item["snippet"]["channelId"],
                    "channel_title": item["snippet"]["channelTitle"],
                    "published_at": item["snippet"]["publishedAt"],
                    "duration_seconds": duration,
                    "duration_minutes": duration / 60,
                    "view_count": views,
                    "like_count": likes,
                    "comment_count": comments,
                    "engagement_rate": engagement_rate,
                    "tags": item["snippet"].get("tags", []),
                    "category_id": item["snippet"].get("categoryId"),
                    "language": item["snippet"].get("defaultLanguage", "unknown"),
                    "made_for_kids": item["status"].get("madeForKids", False)
                }
                videos.append(video_data)
            
            return videos
            
        except HttpError as e:
            self.logger.error(f"HTTP error getting video details: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Error getting video details: {e}")
            return []
    
    def _parse_duration(self, duration_str: str) -> int:
        """Parse ISO 8601 duration string to seconds."""
        # Example: PT4M13S = 4 minutes 13 seconds
        import re
        
        pattern = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
        match = pattern.match(duration_str)
        
        if not match:
            return 0
        
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        
        return hours * 3600 + minutes * 60 + seconds
    
    def get_channel_info(self, channel_ids: List[str]) -> List[Dict[str, Any]]:
        """Get information about YouTube channels."""
        try:
            channel_params = {
                "part": "snippet,statistics,contentDetails",
                "id": ",".join(channel_ids)
            }
            
            response = self.youtube.channels().list(**channel_params).execute()
            
            channels = []
            for item in response["items"]:
                stats = item["statistics"]
                
                channel_data = {
                    "channel_id": item["id"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "created_at": item["snippet"]["publishedAt"],
                    "subscriber_count": int(stats.get("subscriberCount", 0)),
                    "video_count": int(stats.get("videoCount", 0)),
                    "view_count": int(stats.get("viewCount", 0)),
                    "country": item["snippet"].get("country"),
                    "custom_url": item["snippet"].get("customUrl"),
                    "thumbnails": item["snippet"]["thumbnails"]
                }
                channels.append(channel_data)
            
            return channels
            
        except HttpError as e:
            self.logger.error(f"HTTP error getting channel info: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Error getting channel info: {e}")
            return []
    
    def collect_trending_videos(self, 
                              region_code: str = "BR",
                              category_id: Optional[str] = None,
                              max_results: int = 50) -> List[Dict[str, Any]]:
        """Collect trending videos from specified region."""
        try:
            trending_params = {
                "part": "snippet,statistics,contentDetails",
                "chart": "mostPopular",
                "regionCode": region_code,
                "maxResults": max_results
            }
            
            if category_id:
                trending_params["videoCategoryId"] = category_id
            
            response = self.youtube.videos().list(**trending_params).execute()
            
            videos = []
            for item in response["items"]:
                duration = self._parse_duration(item["contentDetails"]["duration"])
                stats = item["statistics"]
                views = int(stats.get("viewCount", 0))
                likes = int(stats.get("likeCount", 0))
                comments = int(stats.get("commentCount", 0))
                
                engagement_rate = (likes + comments) / max(views, 1)
                
                video_data = {
                    "video_id": item["id"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "channel_id": item["snippet"]["channelId"],
                    "channel_title": item["snippet"]["channelTitle"],
                    "published_at": item["snippet"]["publishedAt"],
                    "duration_seconds": duration,
                    "duration_minutes": duration / 60,
                    "view_count": views,
                    "like_count": likes,
                    "comment_count": comments,
                    "engagement_rate": engagement_rate,
                    "category_id": item["snippet"].get("categoryId"),
                    "tags": item["snippet"].get("tags", []),
                    "is_trending": True
                }
                videos.append(video_data)
            
            self.logger.info(f"Collected {len(videos)} trending videos")
            return videos
            
        except HttpError as e:
            self.logger.error(f"HTTP error collecting trending videos: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Error collecting trending videos: {e}")
            return []
    
    def search_by_niche(self, niche: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """Search for videos in a specific niche."""
        niche_queries = {
            "tecnologia": ["tecnologia", "programação", "apps", "gadgets", "inteligência artificial"],
            "educacao": ["educação", "tutorial", "como fazer", "aprender", "curso"],
            "negocios": ["empreendedorismo", "negócios", "marketing", "vendas", "dinheiro"],
            "lifestyle": ["lifestyle", "rotina", "dicas", "vida", "bem-estar"],
            "entretenimento": ["entretenimento", "diversão", "humor", "vlogs", "reacts"]
        }
        
        queries = niche_queries.get(niche, [niche])
        all_videos = []
        
        results_per_query = max_results // len(queries)
        
        for query in queries:
            videos = self.search_videos(query, max_results=results_per_query)
            
            # Get detailed information
            video_ids = [v["video_id"] for v in videos]
            detailed_videos = self.get_video_details(video_ids)
            
            # Add niche information
            for video in detailed_videos:
                video["detected_niche"] = niche
                video["search_query"] = query
            
            all_videos.extend(detailed_videos)
            
            # Rate limiting
            time.sleep(1)
        
        self.logger.info(f"Collected {len(all_videos)} videos for niche: {niche}")
        return all_videos