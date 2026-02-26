# Social Media Marketing Platform

A Django REST Framework and React-based application for managing and scheduling social media posts across multiple platforms (Facebook, Instagram, LinkedIn, X/Twitter).

## Project Overview

The Social Media Marketing Platform simplifies multi-platform social media management by:

- **Unified Post Management**: Create, draft, schedule, and publish posts across multiple social platforms
- **Platform Integration**: Connect multiple social media accounts (Facebook, Instagram, LinkedIn, X/Twitter)
- **Analytics**: Track post performance and engagement metrics
- **Scheduling**: Schedule posts for future publication with automatic task handling
- **User Authentication**: Secure user authentication and OAuth integration for social platforms

---

## Features

✅ **Multi-Platform Support**
- Facebook
- Instagram  
- LinkedIn
- X (Twitter)

✅ **Post Management**
- Create and edit posts
- Draft, schedule, and publish content
- Attach media (images/videos)
- View post status and history

✅ **Account Linking**
- Connect multiple social media accounts
- Store and manage platform tokens securely
- Handle token refresh and expiration

✅ **Analytics Dashboard**
- View post performance metrics
- Track engagement (likes, shares, comments)
- Analyze audience insights

✅ **Async Task Processing**
- Celery integration for background tasks
- Automatic post publishing at scheduled times
- Error handling and retry mechanisms



## Installation & Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- Git
- pip (Python package manager)
- Virtual environment tool (venv)


## API Documentation

### Base URL
```
http://localhost:8000/api
```

### Quick API Reference Table

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| **POST** | `/token/` | Get JWT access token | ❌ No |
| **POST** | `/token/refresh/` | Refresh JWT token | ❌ No |
| **GET** | `/posts/posts/` | List all posts | ✅ Yes |
| **POST** | `/posts/posts/` | Create new post | ✅ Yes |
| **GET** | `/posts/posts/{id}/` | Get single post | ✅ Yes |
| **PATCH** | `/posts/posts/{id}/` | Update post | ✅ Yes |
| **DELETE** | `/posts/posts/{id}/` | Delete post | ✅ Yes |
| **POST** | `/posts/posts/{id}/schedule/` | Schedule post | ✅ Yes |
| **GET** | `/posts/social-accounts/` | List connected accounts | ✅ Yes |
| **POST** | `/posts/social-accounts/` | Connect social account | ✅ Yes |
| **GET** | `/posts/social-accounts/{id}/` | Get account details | ✅ Yes |
| **PATCH** | `/posts/social-accounts/{id}/` | Update account | ✅ Yes |
| **DELETE** | `/posts/social-accounts/{id}/` | Disconnect account | ✅ Yes |

### Authentication

The API uses **JWT (JSON Web Tokens)** and **Token-based authentication**.

**How it works internally**:
1. Backend receives schedule request with future timestamp
2. Post status changed from "draft" to "scheduled"
3. Celery Beat detects scheduled post at specified time
4. Automatically triggers `publish_post_task` in background
5. Task publishes to all connected social accounts
6. Status updated to "published" when complete

---

## API Documentation

### Base URL

```
http://localhost:8000/api
```

### Quick API Reference

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| **POST** | `/token/` | Get JWT token | ❌ |
| **POST** | `/token/refresh/` | Refresh token | ❌ |
| **GET** | `/posts/posts/` | List posts | ✅ |
| **POST** | `/posts/posts/` | Create post | ✅ |
| **GET** | `/posts/posts/{id}/` | Get post | ✅ |
| **PATCH** | `/posts/posts/{id}/` | Update post | ✅ |
| **DELETE** | `/posts/posts/{id}/` | Delete post | ✅ |
| **POST** | `/posts/posts/{id}/schedule/` | Schedule post | ✅ |
| **GET** | `/posts/social-accounts/` | List accounts | ✅ |
| **POST** | `/posts/social-accounts/` | Connect account | ✅ |
| **GET** | `/posts/social-accounts/{id}/` | Get account | ✅ |
| **PATCH** | `/posts/social-accounts/{id}/` | Update account | ✅ |
| **DELETE** | `/posts/social-accounts/{id}/` | Disconnect | ✅ |

---

### Authentication

The API uses **JWT (JSON Web Tokens)** for authentication.


```
Frontend (React)           Backend (Django)          Database
─────────────────          ────────────────          ────────
   User Interface    ────→  REST API Endpoints   ───→ SQLite
   (http://5173)            (http://8000)            db.sqlite3
                            
                            ↓
                         Celery Tasks
                         (background)
                         
                            ↓
                    External APIs
                    (LinkedIn, Facebook, etc.)
```

### Workflow 1: User Authentication

```
1. User enters username & password
   ↓
2. POST /api/token/ with credentials
   ↓
3. Backend validates against database
   ↓
4. Returns access & refresh tokens
   ↓
5. Frontend stores tokens in localStorage
   ↓
6. All subsequent requests include:
   Authorization: Bearer {access_token}
```

### Workflow 2: Connect Social Account

```
1. User clicks "Connect LinkedIn"
   ↓
2. Redirected to LinkedIn OAuth screen
   ↓
3. User grants permission
   ↓
4. LinkedIn sends authorization code
   ↓
5. Frontend sends to backend:
   POST /api/posts/social-accounts/
   {
     "platform": "linkedin",
     "platform_user_id": "...",
     "access_token": "...",
     "refresh_token": "..."
   }
   ↓
6. Backend validates token with LinkedIn API
   ↓
7. Account stored in database
   ↓
8. Frontend shows: "✓ LinkedIn Connected"
```

### Workflow 3: Create & Schedule Post

```
1. User creates post content
   ↓
2. POST /api/posts/posts/ with content
   ↓
3. Backend creates Post object (status: draft)
   ↓
4. User clicks "Schedule"
   ↓
5. POST /api/posts/posts/1/schedule/
   (status changes to: scheduled)
   ↓
6. Celery Beat waits for scheduled time
   ↓
7. At scheduled time:
   - Automatic task triggered
   - Connects to LinkedIn API
   - Connects to Facebook API
   - Connects to Instagram API
   - etc.
   ↓
8. Post published to all platforms
   (status changes to: published)
   ↓
9. Frontend shows: "✓ Published to 3 platforms"
```

### Workflow 4: View Analytics

```
1. User navigates to Analytics
   ↓
2. GET /api/posts/posts/1/
   ↓
3. Backend returns post details with platform_links
   ↓
4. Frontend displays:
   - Post published on: LinkedIn ✓, Facebook ✓
   - Post failed on: Instagram ✗ (token expired)
   ↓
5. User can click to reconnect Instagram
```

---
