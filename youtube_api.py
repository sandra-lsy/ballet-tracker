import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import logging

load_dotenv()

class YouTubeAPI:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            logging.warning("YouTube API key not found. Videos will not load.")
            self.youtube = None
        else:
            try:
                self.youtube = build("youtube", "v3", developerKey=self.api_key)
            except Exception as e:
                logging.error(f"Failed to initialize YouTube API: {e}")
                self.youtube = None

    def search_videos(self, query, max_results=10):
        """Search for videos on YouTube with enhanced error handling"""
        # Return demo videos if API is not available
        if not self.youtube:
            return self._get_demo_videos(query, max_results)

        try:
            search_response = self.youtube.search().list(
                q=query,
                part="id,snippet",
                maxResults=max_results,
                type='video',
                videoDefinition='high',
                order='relevance'
            ).execute()

            videos = []
            for item in search_response['items']:
                # Skip videos with missing thumbnails
                if 'thumbnails' not in item['snippet'] or 'high' not in item['snippet']['thumbnails']:
                    continue
                    
                video = {
                    'id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'][:200] + '...' if len(item['snippet']['description']) > 200 else item['snippet']['description'],
                    'thumbnail': item['snippet']['thumbnails']['high']['url'],
                    'channel': item['snippet']['channelTitle'],
                    'embed_url': f'https://www.youtube.com/embed/{item["id"]["videoId"]}'
                }
                videos.append(video)

            return videos if videos else self._get_demo_videos(query, max_results)
        
        except Exception as e:
            logging.error(f"Error searching for videos: {e}")
            return self._get_demo_videos(query, max_results)

    def _get_demo_videos(self, query, max_results):
        """Return demo videos when API fails"""
        demo_videos = [
            {
                'id': 'demo1',
                'title': f'Demo: {query} Performance',
                'description': 'This is a demo video. Please configure YouTube API key for actual search results.',
                'thumbnail': 'static/images/demo-video.jpg',
                'channel': 'Ballet Tracker Demo',
                'embed_url': 'https://www.youtube.com/embed/33QPDhhyMxw?si=q0sDqHuVb4AQ8nMZ'
            }
        ]
        return demo_videos[:1]
