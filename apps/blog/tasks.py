from celery import shared_task
from django.conf import settings
import logging
import redis
from .models import PostAnalitic, Post



redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)

logger = logging.getLogger(__name__)

@shared_task
def Sync_impressions_to_db():
    
    keys = redis_client.keys("post:impressions:*")
    for key in keys:
        try:
            post_id = key.decode("utf-8").split(":")[-1]
            impressions = int(redis_client.get(key))
            
            post = Post.objects.get(id=post_id)
            analytics, created = PostAnalitic.objects.get_or_create(post=post)
            analytics.impressions += impressions
            analytics.save()
            
            redis_client.delete(key)
        except Exception as e:
            print(f"error al sincronizar la {key}: {str(e)}")
    