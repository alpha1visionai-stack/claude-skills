#!/usr/bin/env python3
"""
Extract transcript from a YouTube video.
"""

import argparse
import sys
from youtube_client import get_video_transcript, get_youtube_service, get_video_info


def main():
    parser = argparse.ArgumentParser(description='Extract YouTube video transcript')
    parser.add_argument('--video-id', required=True, help='YouTube video ID (e.g., dQw4w9WgXcQ)')
    parser.add_argument('--with-metadata', action='store_true', help='Include video metadata')
    parser.add_argument('--output', '-o', help='Output file path (optional)')

    args = parser.parse_args()

    print(f"Extracting transcript for video: {args.video_id}")
    print("-" * 60)

    # Get transcript
    result = get_video_transcript(args.video_id)

    if not result['success']:
        print(f"Error: {result['error']}")
        sys.exit(1)

    # Build output
    output_lines = []

    if args.with_metadata:
        service = get_youtube_service()
        info = get_video_info(service, args.video_id)
        if info['success']:
            output_lines.append(f"Title: {info['title']}")
            output_lines.append(f"Channel: {info['channel_title']}")
            output_lines.append(f"Published: {info['published_at']}")
            output_lines.append("-" * 60)

    output_lines.append(f"Language: {result['language']}")
    output_lines.append(f"Segments: {result['segments']}")
    output_lines.append("-" * 60)
    output_lines.append("TRANSCRIPT:")
    output_lines.append("-" * 60)
    output_lines.append(result['transcript'])

    output_text = '\n'.join(output_lines)

    # Output to file or console
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_text)
        print(f"Transcript saved to: {args.output}")
    else:
        print(output_text)


if __name__ == '__main__':
    main()
