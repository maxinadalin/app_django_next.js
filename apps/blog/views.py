from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Post,Category,Heading
from .serializers import PostSerializer,CategorySerializer,HeadingSerializer
# Create your views here.

class GetCategories(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get(self,request,format=None):
        categorias = Category.objects.all()
        serializer = CategorySerializer(categorias, many = True )
        
        return Response ({"mensaje": serializer.data}, status = status.HTTP_200_OK)