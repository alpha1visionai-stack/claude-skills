import json
import sys

def extract_prompts(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    prompts = []
    
    # Rekursive Suche nach Nutzer-Nachrichten (Pascal)
    def find_user_messages(obj):
        if isinstance(obj, dict):
            if obj.get('role') == 'user' or obj.get('author', {}).get('role') == 'user':
                content = obj.get('content', '')
                if isinstance(content, dict): # Sonnet/ChatGPT JSON Struktur
                    parts = content.get('parts', [])
                    text = "".join([p if isinstance(p, str) else str(p) for p in parts])
                    if text.strip():
                        prompts.append(text.strip())
                elif isinstance(content, str) and content.strip():
                    prompts.append(content.strip())
            for key in obj:
                find_user_messages(obj[key])
        elif isinstance(obj, list):
            for item in obj:
                find_user_messages(item)

    find_user_messages(data)
    return prompts

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_prompts.py <path_to_json>")
        sys.exit(1)
    
    results = extract_prompts(sys.argv[1])
    for i, p in enumerate(results, 1):
        print(f"--- PROMPT {i} ---")
        print(p)
        print()
