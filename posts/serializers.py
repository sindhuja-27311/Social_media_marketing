from rest_framework import serializers
from .models import Post, SocialAccount, PostPlatformLink

class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = '__all__'
        read_only_fields = ('user',)

class PostPlatformLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostPlatformLink
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    platform_links = PostPlatformLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user', 'status', 'published_at')
