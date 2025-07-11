from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostSerializer

import traceback



from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostSerializer


class PostListCreateAPIView(APIView):
    def get(self, request):
        platform = request.GET.get("platform")
        cache_key = f"posts_{platform}" if platform else "posts_all"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        posts = Post.objects.all().order_by("-created_at")
        if platform:
            posts = posts.filter(platforms__contains=[platform])
        serializer = PostSerializer(posts, many=True)

        cache.set(cache_key, serializer.data, timeout=60 * 5)  # cache 5 min
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()

            # Invalidate all cached lists (platform-specific + all)
            cache.delete("posts_all")
            cache.delete("posts_sosioloji")
            cache.delete("posts_wiseandsane")

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


    def patch(self, request, slug):
        post = self.get_object(slug)
        try:
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                cache.delete("posts_all")
                cache.delete("posts_sosioloji")
                cache.delete("posts_wiseandsane")

                updated_post = serializer.save()
                return Response(PostSerializer(updated_post).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()  # This will log the full error to your Django terminal
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, slug):
        post = self.get_object(slug)
        post.delete()
        # Invalidate all cached lists (platform-specific + all)
        cache.delete("posts_all")
        cache.delete("posts_sosioloji")
        cache.delete("posts_wiseandsane")
        return Response({"message": "Post deleted"}, status=status.HTTP_204_NO_CONTENT)
    
