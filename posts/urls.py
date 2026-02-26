from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, SocialAccountViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'social-accounts', SocialAccountViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
