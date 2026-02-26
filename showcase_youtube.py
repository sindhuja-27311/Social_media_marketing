# YouTube Showcase for SMM
import os
import django
from unittest.mock import patch, MagicMock

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_marketing.settings')
django.setup()

from posts.services import YouTubeService

def showcase_youtube():
    print("--- YouTube Backend Showcase ---")
    
    # 1. Verification of Dependencies
    try:
        from googleapiclient.discovery import build
        print("✅ googleapiclient dependency: Installed")
    except ImportError:
        print("❌ googleapiclient dependency: Missing")
        return

    # 2. Showcase posting logic (Mocking the final request for safety)
    print("\nSimulating YouTube Video Upload...")
    service = YouTubeService("mock_access_token_from_oauth")
    
    # Mocking the actual execute() call to see the parameters being passed
    with patch('googleapiclient.discovery.build') as mock_build, \
         patch('googleapiclient.http.MediaFileUpload') as mock_media:
        
        mock_youtube = mock_build.return_value
        mock_videos = mock_youtube.videos.return_value
        mock_insert = mock_videos.insert.return_value
        mock_insert.execute.return_value = {'id': 'youtube_video_id_xyz_123'}
        
        # Test content
        content = "My Awesome Social Media Marketing Demo Video!"
        media_url = "path/to/demo_video.mp4" # This would be a real path in production
        
        print(f"Calling service.publish_post(content='{content}', media_url='{media_url}')")
        result = service.publish_post(content, media_url)
        
        print(f"\nBackend Output: {result}")
        
    # 3. Showcase Analytics logic
    print("\nFetching Simulated YouTube Analytics...")
    stats = service.fetch_analytics()
    print(f"Stats: {stats}")

    print("\n--- Showcase Complete ---")

if __name__ == "__main__":
    showcase_youtube()
