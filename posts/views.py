from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, SocialAccount, PostPlatformLink
from .serializers import PostSerializer, SocialAccountSerializer, PostPlatformLinkSerializer

class SocialAccountViewSet(viewsets.ModelViewSet):
    serializer_class = SocialAccountSerializer
    queryset = SocialAccount.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user)
        if post.status == 'published':
            from .tasks import publish_post_task
            publish_post_task.delay(post.id)

    @action(detail=True, methods=['post'])
    def schedule(self, request, pk=None):
        post = self.get_object()
        scheduled_at = request.data.get('scheduled_at')
        if not scheduled_at:
            return Response({'error': 'scheduled_at is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        post.scheduled_at = scheduled_at
        post.status = 'scheduled'
        post.save()
        
        from .tasks import publish_post_task
        # In a real app, we'd use eta=scheduled_at
        publish_post_task.apply_async((post.id,), eta=post.scheduled_at)
        
        return Response({'status': 'post scheduled'})
