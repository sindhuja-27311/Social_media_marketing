from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SocialAccount(models.Model):
    PLATFORM_CHOICES = (
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('x', 'X (Twitter)'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_accounts')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    platform_user_id = models.CharField(max_length=255)
    access_token = models.TextField()
    refresh_token = models.TextField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.platform}"

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    media_url = models.URLField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.user.username} - {self.status}"

class PostPlatformLink(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='platform_links')
    social_account = models.ForeignKey(SocialAccount, on_delete=models.CASCADE)
    platform_post_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Post.STATUS_CHOICES, default='draft')
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.post.id} linked to {self.social_account.platform}"
