import os
import django
from unittest.mock import patch

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_marketing.settings')
django.setup()

from posts.services import YouTubeService

def test_youtube_auth():
    print("Verifying YouTube Credentials...")
    
    # In YouTubeService, authenticate() just checks if access_token is present.
    # However, to REALLY check if keys are working, we'd need a real OAuth flow.
    # We can at least check if the settings are correctly picking up the .env values.
    from django.conf import settings
    
    client_id = getattr(settings, 'YOUTUBE_CLIENT_ID', None)
    client_secret = getattr(settings, 'YOUTUBE_CLIENT_SECRET', None)
    
    if client_id and client_id != 'your_youtube_client_id' and client_secret and client_secret != 'your_youtube_client_secret':
        print(f"✅ YouTube Client ID found: {client_id[:10]}...")
        print(f"✅ YouTube Client Secret found: {client_secret[:5]}...")
        
        # Test basic service instantiation
        service = YouTubeService("dummy_token")
        if service.authenticate():
            print("✅ Service authenticated successfully (token check passed).")
        else:
            print("❌ Service authentication failed.")
    else:
        print("❌ YouTube credentials missing or still placeholders in .env")

if __name__ == "__main__":
    test_youtube_auth()
