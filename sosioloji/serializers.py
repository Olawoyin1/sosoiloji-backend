from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id", "title", "author", "category", "subtag", "slug",
            "quote", "body", "image", "video", "content_images", "blogcontentvideo",
            "created_at", "platforms",'callout', 'product_card'  
        ]
        read_only_fields = ["slug", "created_at"]
        
