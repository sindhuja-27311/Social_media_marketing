# Standalone Test Script for Social Media Services
import os
import django
from unittest.mock import patch, MagicMock

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_marketing.settings')
django.setup()

from posts.services import SocialMediaManager

def run_tests():
    print("Starting Social Media Service Verification...")
    
    # 1. Test LinkedIn
    print("\nTesting LinkedIn Service...")
    with patch('requests.get') as mock_get, patch('requests.post') as mock_post:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'id': 'user_123'}
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {'id': 'urn:li:share:123'}
        
        result = SocialMediaManager.publish('linkedin', 'fake_token', 'Test post')
        print(f"Result: {result}")

    # 2. Test Facebook
    print("\nTesting Facebook Service...")
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'id': 'fb_post_123'}
        
        result = SocialMediaManager.publish('facebook', 'fake_token', 'Test post')
        print(f"Result: {result}")

    # 3. Test Instagram
    print("\nTesting Instagram Service...")
    with patch('requests.post') as mock_post:
        mock_post.side_effect = [
            MagicMock(status_code=200, json=lambda: {'id': 'cont_123'}),
            MagicMock(status_code=200, json=lambda: {'id': 'ig_post_123'})
        ]
        
        result = SocialMediaManager.publish('instagram', 'fake_token', 'Test caption', media_url='http://image.jpg')
        print(f"Result: {result}")

    # 4. Test YouTube
    print("\nTesting YouTube Service...")
    result = SocialMediaManager.publish('youtube', 'fake_token', 'Test video')
    print(f"Result: {result}")

    print("\nVerification Complete.")

if __name__ == "__main__":
    run_tests()
