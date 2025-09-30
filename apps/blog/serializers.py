from rest_framework import serializers
from .models import Category, Post, Heading

class CategorySerializer(serializers.ModelSerializer):
    class Meta():
        model: Category
        fields = (
           "__all__"
        )

class PostSerializer(serializers.ModelSerializer):
    class Meta():
        model: Post
        fields = (
           "__all__"
        )
        
class HeadingSerializer(serializers.ModelSerializer):
    class Meta():
        model: Heading
        fields = (
           "__all__"
        )