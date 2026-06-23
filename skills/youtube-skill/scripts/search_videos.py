#!/usr/bin/env python3
"""
Search YouTube videos by query.
"""

import argparse
import json
from youtube_client import get_youtube_service, search_videos


def main():
    parser = argparse.ArgumentParser(description='Search YouTube videos')
    parser.add_argument('--query', '-q', required=True, help='Search query')
    parser.add_argument('--max-results', type=int, default=10, help='Maximum results (default: 10)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--output', '-o', help='Output file (optional)')

    args = parser.parse_args()

    print(f"Searching YouTube for: '{args.query}'")
    print("-" * 60)

    service = get_youtube_service()
    result = search_videos(service, args.query, args.max_results)

    if not result['success']:
        print(f"Error: {result['error']}")
        return

    videos = result['videos']

    if not videos:
        print("No videos found.")
        return

    # Format output
    if args.json:
        output = json.dumps(videos, indent=2)
    else:
        lines = []
        for i, video in enumerate(videos, 1):
            lines.append(f"{i}. {video['title']}")
            lines.append(f"   Channel: {video['channel_title']}")
            lines.append(f"   Published: {video['published_at'][:10]}")
            lines.append(f"   Video ID: {video['id']}")
            lines.append(f"   https://youtube.com/watch?v={video['id']}")
            lines.append(f"   {video['description'][:100]}..." if len(video['description']) > 100 else f"   {video['description']}")
            lines.append("")

        output = '\n'.join(lines)

    # Output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Results saved to: {args.output}")
    else:
        print(f"Found {len(videos)} videos:\n")
        print(output)


if __name__ == '__main__':
    main()
