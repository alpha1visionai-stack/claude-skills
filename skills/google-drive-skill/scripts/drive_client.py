"""
Google Drive API Client - Shared authentication and utilities
"""

import os
import pickle
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# If modifying scopes, delete token.json
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


def get_credentials():
    """Get or refresh OAuth2 credentials for Google Drive API."""
    creds = None
    token_path = os.getenv('GOOGLE_DRIVE_TOKEN_PATH', 'token.json')
    credentials_path = os.getenv('GOOGLE_DRIVE_CREDENTIALS_PATH', 'credentials.json')

    # Load existing token
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # Refresh or create new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(
                    f"credentials.json not found at {credentials_path}. "
                    "Download from Google Cloud Console."
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for future runs
        os.makedirs(os.path.dirname(token_path) or '.', exist_ok=True)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def get_drive_service():
    """Build and return the Google Drive API service."""
    creds = get_credentials()
    return build('drive', 'v3', credentials=creds)


def list_files(service, folder_id=None, max_results=100, query=None):
    """List files in Drive or specific folder."""
    results = []
    page_token = None

    # Build query string
    q = query or ""
    if folder_id:
        folder_query = f"'{folder_id}' in parents"
        q = f"{folder_query} and {q}" if q else folder_query

    while len(results) < max_results:
        try:
            response = service.files().list(
                q=q if q else None,
                spaces='drive',
                fields='nextPageToken, files(id, name, mimeType, modifiedTime, size)',
                pageToken=page_token,
                pageSize=min(100, max_results - len(results))
            ).execute()

            results.extend(response.get('files', []))
            page_token = response.get('nextPageToken')

            if not page_token or len(results) >= max_results:
                break

        except HttpError as e:
            print(f"API Error: {e}")
            break

    return results[:max_results]


def download_file(service, file_id, output_path):
    """Download a file from Google Drive."""
    from googleapiclient.http import MediaIoBaseDownload
    import io

    try:
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(output_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%")

        return True
    except HttpError as e:
        print(f"Download failed: {e}")
        return False


def upload_file(service, file_path, folder_id=None, mime_type=None):
    """Upload a file to Google Drive."""
    from googleapiclient.http import MediaFileUpload

    file_metadata = {'name': Path(file_path).name}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        return file
    except HttpError as e:
        print(f"Upload failed: {e}")
        return None
