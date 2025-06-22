from django.db import models
from django.utils.text import slugify

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)  # ✅ new field
    author = models.CharField(max_length=255)
    body = models.TextField()
    category = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    subtag = models.CharField(max_length=100, blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    contentImages = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Ensure uniqueness
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
