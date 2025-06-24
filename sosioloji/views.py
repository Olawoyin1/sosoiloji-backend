from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostSerializer


# GET all posts & POST new post
class PostListCreateAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all().order_by("-created_at")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()  # slug is generated in model
            return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET single post by slug, UPDATE post by slug, DELETE post by slug
class PostDetailAPIView(APIView):
    def get_object(self, slug):
        return get_object_or_404(Post, slug=slug)

    def get(self, request, slug):
        post = self.get_object(slug)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, slug):
        post = self.get_object(slug)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Note: slug is not regenerated here
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        post = self.get_object(slug)
        post.delete()
        return Response({"message": "Post deleted"}, status=status.HTTP_204_NO_CONTENT)
