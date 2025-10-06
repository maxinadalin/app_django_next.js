from rest_framework import serializers
from .models import Category, Post, Heading, PostViews

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields ="__all__"
        


class PostViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostViews
        fields = '__all__'
        
        
class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    view_count = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields =  "__all__"
        
    def get_view_count(self,obj):
        return obj.post_View.count()
        
        
class HeadingSerializer(serializers.ModelSerializer):
    class Meta:
        model= Heading
        fields = "__all__"
        
        

