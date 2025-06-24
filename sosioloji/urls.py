from django.urls import path
from .views import PostListCreateAPIView, PostDetailAPIView

urlpatterns = [
    path("posts/", PostListCreateAPIView.as_view(), name="post-list-create"),
    path("posts/<slug:slug>/", PostDetailAPIView.as_view(), name="post-detail"),
]
