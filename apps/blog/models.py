from django.db import models
from django.utils import timezone
# Create your models here.

def thumbnail_blog(instance,filename):
    return "blog/{0}/{1}".format(instance.title,filename)


class Post(models.Model):
    
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status="published")
    
    status_options = (
        ("draft", "Draft")
        ("published", "Published")
    )
    
    tittle = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to=thumbnail_blog)
    keywords = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=10, choices=status_options, default="draft")
    
    objects = models.Manager()
    postobject = PostObjects()
    
    class Meta:
        ordering = ("-published")
        
    def __str__(self):
        return self.tittle
    