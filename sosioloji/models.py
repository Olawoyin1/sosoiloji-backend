from django.db import models
from django.utils.text import slugify



PLATFORM_CHOICES = (
    ("sosioloji", "Sosioloji"),
    ("wiseandsane", "Wise and Sane"),
)

class Post(models.Model):
    platforms = models.JSONField(default=list, blank=True) 
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    subtag = models.CharField(max_length=100, blank=True, null=True)
    quote = models.TextField(blank=True)
    body = models.TextField()
    image = models.URLField(blank=True)
    video = models.URLField(blank=True)
    content_images = models.JSONField(default=list, blank=True)
    blogcontentvideo = models.URLField(blank=True)
    
    callout = models.JSONField(blank=True, null=True)
    product_card = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
