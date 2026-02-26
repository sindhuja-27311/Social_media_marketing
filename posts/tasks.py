from celery import shared_task
from .models import Post, PostPlatformLink
from .services import SocialMediaManager
import logging

logger = logging.getLogger(__name__)

@shared_task
def publish_post_task(post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        logger.error(f"Post {post_id} does not exist")
        return

    # If the post is already published or failed, we might want to skip or retry
    # For now, let's process its links
    links = PostPlatformLink.objects.filter(post=post)
    
    if not links.exists():
        # If no links, maybe create them for all user's accounts?
        # For now, we assume links are created when scheduling/publishing
        logger.info(f"No platform links for post {post_id}")
        return

    all_success = True
    for link in links:
        if link.status == 'published':
            continue
            
        try:
            account = link.social_account
            result = SocialMediaManager.publish(
                platform=account.platform,
                access_token=account.access_token,
                content=post.content,
                media_url=post.media_url
            )
            
            if result['status'] == 'success':
                link.status = 'published'
                link.platform_post_id = result['platform_post_id']
                link.save()
            else:
                link.status = 'failed'
                link.error_message = result.get('error', 'Unknown error')
                link.save()
                all_success = False
        except Exception as e:
            logger.error(f"Failed to publish to {link.social_account.platform}: {str(e)}")
            link.status = 'failed'
            link.error_message = str(e)
            link.save()
            all_success = False

    if all_success:
        post.status = 'published'
    else:
        post.status = 'failed'
    post.save()
