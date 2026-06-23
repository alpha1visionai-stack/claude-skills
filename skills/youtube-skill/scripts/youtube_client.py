"""
YouTube API Client - Shared authentication and utilities
"""

import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_youtube_service():
    """Build and return the YouTube Data API service."""
    api_key = os.getenv('YOUTUBE_API_KEY')

    if not api_key or api_key == 'your_youtube_api_key_here'::
        raise ValueError(
            "YOUTUBE_API_KEY not set in .env file. "
            "Get your API key from https://console.cloud.google.com/"
        )

    return build('youtube', 'v3', developerKey=api_key)


def get_video_transcript(video_id):
    """Extract transcript from a YouTube video."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

        # Combine all transcript pieces
        full_transcript = ' '.join([item['text'] for item in transcript_list])

        return {
            'success': True,
            'transcript': full_transcript,
            'language': transcript_list[0].get('language', 'unknown') if transcript_list else 'unknown',
            'segments': len(transcript_list)
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'transcript': None
        }


def get_video_info(service, video_id):
    """Get detailed information about a YouTube video."""
    try:
        response = service.videos().list(
            part='snippet,contentDetails,statistics',
            id=video_id
        ).execute()

        if not response['items']:
            return {'success': False, 'error': 'Video not found'}

        video = response['items'][0]
        snippet = video['snippet']
        stats = video.get('statistics', {})

        return {
            'success': True,
            'id': video_id,
            'title': snippet['title'],
            'description': snippet['description'],
            'published_at': snippet['publishedAt'],
            'channel_title': snippet['channelTitle'],
            'channel_id': snippet['channelId'],
            'tags': snippet.get('tags', []),
            'view_count': stats.get('viewCount', 'N/A'),
            'like_count': stats.get('likeCount', 'N/A'),
            'comment_count': stats.get('commentCount', 'N/A'),
            'duration': video['contentDetails']['duration']
        }
    except HttpError as e:
        return {'success': False, 'error': str(e)}


def search_videos(service, query, max_results=10):
    """Search for YouTube videos by query."""
    try:
        response = service.search().list(
            part='snippet',
            q=query,
            type='video',
            maxResults=max_results
        ).execute()

        videos = []
        for item in response.get('items', []):
            videos.append({
                'id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'][:200] + '...' if len(item['snippet']['description']) > 200 else item['snippet']['description'],
                'channel_title': item['snippet']['channelTitle'],
                'published_at': item['snippet']['publishedAt'],
                'thumbnail': item['snippet']['thumbnails']['default']['url']
            })

        return {'success': True, 'videos': videos, 'total_results': len(videos)}
    except HttpError as e:
        return {'success': False, 'error': str(e)}


def get_channel_info(service, channel_id):
    """Get information about a YouTube channel."""
    try:
        response = service.channels().list(
            part='snippet,statistics',
            id=channel_id
        ).execute()

        if not response['items']:
            return {'success': False, 'error': 'Channel not found'}

        channel = response['items'][0]
        snippet = channel['snippet']
        stats = channel.get('statistics', {})

        return {
            'success': True,
            'id': channel_id,
            'title': snippet['title'],
            'description': snippet['description'],
            'custom_url': snippet.get('customUrl', 'N/A'),
            'published_at': snippet['publishedAt'],
            'subscriber_count': stats.get('subscriberCount', 'N/A'),
            'video_count': stats.get('videoCount', 'N/A'),
            'view_count': stats.get('viewCount', 'N/A')
        }
    except HttpError as e:
        return {'success': False, 'error': str(e)}
