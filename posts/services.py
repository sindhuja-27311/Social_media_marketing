import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class BaseSocialService:
    def __init__(self, access_token=None):
        self.access_token = access_token

    def authenticate(self):
        """Logic to handle initial authentication or token validation."""
        raise NotImplementedError

    def publish_post(self, content, media_url=None):
        """Logic to publish content to the platform."""
        raise NotImplementedError

    def fetch_analytics(self):
        """Logic to fetch basic analytics like likes or shares."""
        raise NotImplementedError

class LinkedInService(BaseSocialService):
    def authenticate(self):
        # Basic validation: check if token can fetch profile
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get("https://api.linkedin.com/v2/me", headers=headers)
        return response.status_code == 200

    def publish_post(self, content, media_url=None):
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0",
            }
            # Get user URN
            user_info = requests.get("https://api.linkedin.com/v2/me", headers=headers).json()
            user_urn = user_info.get("id")
            
            if not user_urn:
                 return {"status": "failed", "error": "Could not retrieve LinkedIn URN"}

            post_data = {
                "author": f"urn:li:person:{user_urn}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": content},
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
            }
            
            response = requests.post("https://api.linkedin.com/v2/ugcPosts", headers=headers, json=post_data)
            if response.status_code == 201:
                return {"status": "success", "platform_post_id": response.json().get('id')}
            return {"status": "failed", "error": response.text}
        except Exception as e:
            logger.error(f"LinkedIn error: {str(e)}")
            return {"status": "failed", "error": str(e)}

    def fetch_analytics(self):
        # Placeholder for LinkedIn analytics API
        return {"likes": 0, "shares": 0, "comments": 0}

class FacebookService(BaseSocialService):
    def __init__(self, access_token=None):
        super().__init__(access_token)
        # Usually requires a Page Access Token for business posting
        self.page_access_token = getattr(settings, 'FACEBOOK_PAGE_ACCESS_TOKEN', None) or access_token
        self.base_url = "https://graph.facebook.com/v19.0"

    def authenticate(self):
        if not self.page_access_token:
            return False
        response = requests.get(f"{self.base_url}/me?access_token={self.page_access_token}")
        return response.status_code == 200

    def publish_post(self, content, media_url=None):
        try:
            params = {
                "message": content,
                "access_token": self.page_access_token
            }
            if media_url:
                params["link"] = media_url
            
            # Post to page feed
            response = requests.post(f"{self.base_url}/me/feed", params=params)
            if response.status_code == 200:
                return {"status": "success", "platform_post_id": response.json().get('id')}
            return {"status": "failed", "error": response.text}
        except Exception as e:
            logger.error(f"Facebook error: {str(e)}")
            return {"status": "failed", "error": str(e)}

    def fetch_analytics(self):
        return {"reactions": 0, "comments": 0, "shares": 0}

class InstagramService(BaseSocialService):
    def __init__(self, access_token=None):
        super().__init__(access_token)
        self.business_id = getattr(settings, 'INSTAGRAM_BUSINESS_ID', '')
        self.base_url = "https://graph.facebook.com/v19.0"

    def authenticate(self):
        return bool(self.business_id and self.access_token)

    def publish_post(self, content, media_url=None):
        # Instagram requires a media container first
        if not media_url:
            return {"status": "failed", "error": "Instagram requires a media_url (image/video)"}
        try:
            # 1. Create media container
            container_url = f"{self.base_url}/{self.business_id}/media"
            container_data = {
                "image_url": media_url,
                "caption": content,
                "access_token": self.access_token
            }
            res = requests.post(container_url, data=container_data).json()
            creation_id = res.get('id')
            
            if not creation_id:
                return {"status": "failed", "error": f"Container creation failed: {res}"}

            # 2. Publish container
            publish_url = f"{self.base_url}/{self.business_id}/media_publish"
            publish_data = {
                "creation_id": creation_id,
                "access_token": self.access_token
            }
            final_res = requests.post(publish_url, data=publish_data).json()
            return {"status": "success", "platform_post_id": final_res.get('id')}
        except Exception as e:
            logger.error(f"Instagram error: {str(e)}")
            return {"status": "failed", "error": str(e)}

    def fetch_analytics(self):
        return {"impressions": 0, "reach": 0, "engagement": 0}

class YouTubeService(BaseSocialService):
    def authenticate(self):
        return bool(self.access_token)

    def publish_post(self, content, media_url=None):
        """
        In YouTube, 'publishing' means uploading a video.
        Note: This requires the google-api-python-client library.
        """
        if not media_url:
            return {"status": "failed", "error": "YouTube requires a media_url (video file link or path)."}
        
        try:
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload
            from google.oauth2.credentials import Credentials

            # Use the access_token to build the YouTube service
            creds = Credentials(self.access_token)
            youtube = build("youtube", "v3", credentials=creds)

            # For a real implementation, media_url should be a local path or we download it
            # For this showcase, we'll assume media_url is a path to a video
            media = MediaFileUpload(media_url, chunksize=-1, resumable=True)
            
            request = youtube.videos().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": content[:100], # YouTube title limit
                        "description": content,
                        "tags": ["SMM", "SocialMedia"]
                    },
                    "status": {
                        "privacyStatus": "public"
                    }
                },
                media_body=media
            )
            
            response = request.execute()
            return {"status": "success", "platform_post_id": response.get('id')}
        except ImportError:
            return {"status": "failed", "error": "google-api-python-client not installed."}
        except Exception as e:
            logger.error(f"YouTube error: {str(e)}")
            return {"status": "failed", "error": str(e)}

    def fetch_analytics(self):
        if not self.access_token:
            return {"views": 0, "likes": 0, "comments": 0}
        try:
            from googleapiclient.discovery import build
            from google.oauth2.credentials import Credentials
            creds = Credentials(self.access_token)
            youtube = build("youtube", "v3", credentials=creds)
            # Fetch channel or video statistics
            return {"views": 120, "likes": 15, "comments": 2} # Mocked for showcase
        except Exception:
            return {"views": 0, "likes": 0, "comments": 0}

class SocialMediaManager:
    SERVICES = {
        'linkedin': LinkedInService,
        'facebook': FacebookService,
        'instagram': InstagramService,
        'youtube': YouTubeService,
    }

    @classmethod
    def get_service(cls, platform, access_token):
        service_class = cls.SERVICES.get(platform.lower())
        if not service_class:
            raise ValueError(f"Platform {platform} not supported")
        return service_class(access_token)

    @classmethod
    def publish(cls, platform, access_token, content, media_url=None):
        service = cls.get_service(platform, access_token)
        return service.publish_post(content, media_url)
