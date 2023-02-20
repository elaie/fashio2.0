from .models import Post
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.decorators import permission_classes

# Create your views here.

class PostView(APIView):

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PostDetailView(APIView):

    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PostCreateView(APIView):

    def post(self, request):
        user = request.user
        data = request.data

        post = {
            "post_name": data["post_name"],
            "post_bio": data["post_bio"],
            "post_likes": data["post_likes"],
            "post_comment": data["post_comment"],
            "post_image": data["post_image"],
        }

        serializer = PostSerializer(data=post, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


       
class PostEditView(APIView):
    
    def put(self, request, pk):
        data = request.data
        post = Post.objects.get(id=pk)
        
        updated_post = {
            "post_name": data["post_name"] if data["post_name"] else post.post_name,
            "post_bio": data["post_bio"] if data["post_bio"] else post.post_bio,
            "post_likes": data["post_likes"] if data["post_likes"] else post.post_likes,
            "post_comment": data["post_comment"] if data["post_comment"] else post.post_comment,
            "post_image": data["post_image"] if data["post_image"] else post.post_image, 
        }
        serializer = PostSerializer(post, data=updated_post)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
      
        

class PostDeleteView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            post.delete()
            return Response({"detail": "Product successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
