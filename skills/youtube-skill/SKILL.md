---
name: youtube-skill
description: Use when extracting YouTube video transcripts, retrieving video metadata, or searching YouTube content programmatically from Claude Code.
---

# YouTube Skill

## Overview
Python-based skill for YouTube Data API v3 and transcript extraction. Direct API integration without MCP overhead.

## When to Use
- Extract video transcripts for analysis
- Retrieve video metadata (title, description, publish date)
- Search YouTube videos by keyword
- Get channel information and playlists
- Download video information for research

## Requirements

1. **Google Cloud Project**: https://console.cloud.google.com/
2. **Enable YouTube Data API v3**: APIs & Services > Library > YouTube Data API v3
3. **Create API Key**: APIs & Services > Credentials > Create API Key
4. **Copy API key** to `.env` file

## Quick Reference

| Operation | Script | Example |
|-----------|--------|---------|
| Get transcript | get_transcript.py | `--video-id <id>` |
| Video metadata | get_video_info.py | `--video-id <id>` |
| Search videos | search_videos.py | `--query "python tutorial"` |
| Channel info | get_channel.py | `--channel-id <id>` |

## Setup

### 1. Environment Variables (.env)
```
YOUTUBE_API_KEY=your_api_key_here
```

### 2. Usage
```bash
python scripts/get_transcript.py --video-id "dQw4w9WgXcQ"
python scripts/search_videos.py --query "Claude AI tutorial" --max-results 10
```

## API Quota Notes
- YouTube API has quota limits (10,000 units/day for new projects)
- Search: 100 units per request
- Video info: 1 unit per request
- Transcript extraction: No quota (uses youtube-transcript-api library)

## Error Handling
- **Quota exceeded**: Script waits and retries or suggests alternative
- **Video unavailable**: Returns clear error message
- **Transcript disabled**: Falls back to metadata only

## Security Notes
- API key stored in `.env`, never commit to version control
- Read-only operations (no uploads or modifications)
