#!/usr/bin/env python3
"""
List files in Google Drive folder.
"""

import argparse
import json
from drive_client import get_drive_service, list_files


def format_size(size_bytes):
    """Format file size for display."""
    if not size_bytes:
        return "N/A"
    try:
        size = int(size_bytes)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    except:
        return "N/A"


def main():
    parser = argparse.ArgumentParser(description='List files in Google Drive')
    parser.add_argument('--folder-id', help='Folder ID to list (default: root)')
    parser.add_argument('--max-results', type=int, default=50, help='Maximum results (default: 50)')
    parser.add_argument('--query', help='Additional search query')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--output', '-o', help='Output file (optional)')

    args = parser.parse_args()

    print("Connecting to Google Drive...")
    service = get_drive_service()

    print(f"Listing files{' in folder ' + args.folder_id if args.folder_id else ''}...")
    files = list_files(service, folder_id=args.folder_id, max_results=args.max_results, query=args.query)

    if not files:
        print("No files found.")
        return

    # Format output
    if args.json:
        output = json.dumps(files, indent=2)
    else:
        lines = []
        lines.append(f"{'Name':<50} {'Type':<20} {'Size':<12} {'ID':<30}")
        lines.append("-" * 112)

        for file in files:
            name = file['name'][:48] if len(file['name']) > 48 else file['name']
            mime = file['mimeType'].split('.')[-1][:18] if '.' in file['mimeType'] else file['mimeType'][:18]
            size = format_size(file.get('size'))
            file_id = file['id'][:28]
            lines.append(f"{name:<50} {mime:<20} {size:<12} {file_id:<30}")

        output = '\n'.join(lines)

    # Output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"\nOutput saved to: {args.output}")
    else:
        print(f"\nFound {len(files)} files:\n")
        print(output)


if __name__ == '__main__':
    main()
