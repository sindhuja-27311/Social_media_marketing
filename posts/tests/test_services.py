from django.test import TestCase
from unittest.mock import patch, MagicMock
from ..services import SocialMediaManager, LinkedInService, FacebookService, InstagramService, YouTubeService

class SocialMediaServiceTest(TestCase):
    def test_manager_get_services(self):
        self.assertIsInstance(SocialMediaManager.get_service('linkedin', 'token'), LinkedInService)
        self.assertIsInstance(SocialMediaManager.get_service('facebook', 'token'), FacebookService)
        self.assertIsInstance(SocialMediaManager.get_service('instagram', 'token'), InstagramService)
        self.assertIsInstance(SocialMediaManager.get_service('youtube', 'token'), YouTubeService)

    @patch('requests.get')
    @patch('requests.post')
    def test_linkedin_publish_success(self, mock_post, mock_get):
        mock_get.return_value.json.return_value = {'id': 'user123'}
        mock_get.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'id': 'link123'}
        mock_post.return_value.status_code = 201
        
        service = LinkedInService('token')
        result = service.publish_post("Hello LinkedIn")
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['platform_post_id'], 'link123')

    @patch('requests.post')
    def test_facebook_publish_success(self, mock_post):
        mock_post.return_value.json.return_value = {'id': 'fb123'}
        mock_post.return_value.status_code = 200
        
        service = FacebookService('token')
        result = service.publish_post("Hello FB")
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['platform_post_id'], 'fb123')

    @patch('requests.post')
    def test_instagram_publish_success(self, mock_post):
        # Mock container creation and publishing
        mock_post.side_effect = [
            MagicMock(status_code=200, json=lambda: {'id': 'cont123'}),
            MagicMock(status_code=200, json=lambda: {'id': 'ig123'})
        ]
        
        service = InstagramService('token')
        result = service.publish_post("Hello IG", media_url="http://example.com/img.jpg")
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['platform_post_id'], 'ig123')

    def test_authenticate_methods(self):
         with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            self.assertTrue(FacebookService('token').authenticate())
            self.assertTrue(LinkedInService('token').authenticate())
            self.assertTrue(InstagramService('token').authenticate())
            self.assertTrue(YouTubeService('token').authenticate())
