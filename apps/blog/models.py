from django.db import models
from django.utils import timezone
import uuid
from django.utils.text import slugify

# Create your models here.

def thumbnail_blog(instance,filename):
    return "blog/{0}/{1}".format(instance.title,filename)

def thumbnail_blog_category(instance,filename):
    return "blog_category/{0}/{1}".format(instance.name,filename)


class Category(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    parent = models.ForeignKey("self",related_name="children",on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to=thumbnail_blog_category)
    slug = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
       


class Post(models.Model):
    
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status="published")
    
    status_options = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=100)
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
    
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    
    class Meta:
        ordering = ("status","-created_at")
        
    def __str__(self):
        return self.tittle

class Heading(models.Model):
    
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    post = models.ForeignKey(Post,on_delete=models.PROTECT, related_name="heading")
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=50)
    
    level = models.IntegerField(
        choices=(
            (1,"H1"),
            (2,"H2"),
            (3,"H3"),
            (4,"H4"),
            (5,"H5"),
            (6,"H6"),
        )
    )
    order = models.PositiveIntegerField()
    
    class Meta:
        ordering = ["order"]
        
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)    
        