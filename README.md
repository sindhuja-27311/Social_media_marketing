📣 Social Media Marketing Backend

A scalable Django microservice for multi-platform social media publishing and scheduling.

🛠️ Built With

Django

Django REST Framework

Celery

Redis

PostgreSQL

🚀 Features

🔐 Connect multiple social media accounts

📝 Create and manage posts

⏳ Schedule posts with background processing

📊 Track per-platform publishing status

❌ Platform-specific error handling

🧩 Easily extensible architecture

🏗️ Architecture Overview
Core Models
SocialAccount

Stores platform credentials (access tokens).

Post

Represents the master content created by the user.

PostPlatformLink

Tracks publishing status of a Post on a specific platform.

This enables independent platform tracking:

Same Post → Published on LinkedIn
Same Post → Failed on Facebook
🔄 Publishing Flow
1. Create Post → /posts/
2. (Optional) Schedule → /posts/{id}/schedule/
3. Celery processes background task
4. Platform-specific service publishes content
5. Status stored per platform
🌍 Supported Platforms

Facebook – Page Feed publishing

Instagram – Media Container → Publish flow

LinkedIn – UGC API integration

YouTube – Video upload via Google API

📡 API Endpoints
🔐 Social Accounts
Method	Endpoint
GET	/social-accounts/
POST	/social-accounts/
DELETE	/social-accounts/{id}/
📝 Posts
Method	Endpoint
GET	/posts/
POST	/posts/
GET	/posts/{id}/
PATCH	/posts/{id}/
DELETE	/posts/{id}/
⏳ Schedule Post
POST /posts/{id}/schedule/
{
  "scheduled_at": "2024-12-25T10:00:00Z"
}
⚙️ Background Tasks

Celery + Redis

Asynchronous publishing

Platform-level error tracking

🧩 Extending to New Platforms
1. Create a new service class inheriting BaseSocialService
2. Implement publish() method
3. Register it inside SocialMediaManager

Done ✅

📦 Production Stack

Gunicorn

Nginx

PostgreSQL

Redis

Celery Workers

📌 Summary

This backend provides a clean, scalable, and production-ready system for managing multi-platform social media publishing with full per-platform status tracking.
