from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Post,Category,Heading,PostViews
from .serializers import PostSerializer,CategorySerializer,HeadingSerializer,PostViewSerializer
from .utils import get_client_ip
class GetCategories(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get(self,request,format=None):
        if Category.objects.all().exists():
            categorias = Category.objects.all()
            serializer = CategorySerializer(categorias, many = True )
        
            return Response ({"mensaje": serializer.data}, status = status.HTTP_200_OK)
        else:
            return Response({"mensaje": "no se encontraron categorias"}, status = status.HTTP_404_NOT_FOUND)
        

class GetPost(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get(self,request,id,format=None):
        if Post.objects.filter(id = id).exists():
            post = Post.objects.get(id=id)
            serializer = PostSerializer(post,)
            client_ip = get_client_ip(request)
            if PostViews.objects.filter(post=post, ip_address=client_ip).exists():
                return Response(serializer.data)
            
            PostViews.objects.create(
                post=post,
                ip_address=client_ip
            )
            
            
        
            return Response ({"mensaje": serializer.data}, status = status.HTTP_200_OK)
        else:
            return Response({"mensaje": "no se encontraron categorias"}, status = status.HTTP_404_NOT_FOUND)