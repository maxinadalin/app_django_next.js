from django.db import models
from django.utils import timezone
import uuid
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from rest_framework import serializers
from .utils import get_client_ip
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

def thumbnail_blog(instance,filename):
    return "blog/{0}/{1}".format(instance.title,filename)

def thumbnail_blog_category(instance,filename):
    return "blog_category/{0}/{1}".format(instance.name,filename)


class Category(models.Model):
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
    
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
    content = CKEditor5Field('content', config_name='default')
    thumbnail = models.ImageField(upload_to=thumbnail_blog)
    keywords = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=10, choices=status_options, default="draft")
    
    objects = models.Manager()
    postobject = PostObjects()
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    
    class Meta:
        ordering = ("status","-created_at")
        
    def __str__(self):
        return self.title

class PostViews(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="post_View")
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    

class Heading(models.Model):
    
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="heading")
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
        
        
        
        
        

class PostAnalitic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="post_Analitics")
    views = models.PositiveIntegerField(default =0)
    impressions = models.PositiveIntegerField(default =0)
    clicks= models.PositiveIntegerField(default =0)
    click_through_rate = models.FloatField(default=0)
    avg_time_on_page = models.FloatField(default=0)
    
    def increment_click(self):
        self.click +=1
        self._update_click_through_rate()
        
    def _update_click_through_rate(self):
        if self.impressions > 0:
            self.click_through_rate = (self.click/self.impressions)*100
    
    def increment_impressions(self):
        self.impressions += 1
        self._update_click_through_rate()
        
    def increment_views(self,request):
        ip_address = get_client_ip(request)
        
        if not PostViews.objects.filter(post=self.post,ip_address=ip_address).exists():
            self.views += 1
            self.save()
    
    
    
    
    
@receiver(post_save, sender=Post)
def _create_post_analitics(sender,instance,created, **kwargs):
    if created:
        PostAnalitic.objects.create(post=instance)
