from django.urls import path
from .views import BlogPostListCreateAPIView, BlogPostDetailAPIView

urlpatterns = [
    path('posts/', BlogPostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', BlogPostDetailAPIView.as_view(), name='post-detail'),
]
