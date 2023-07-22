from django.shortcuts import render
from django.contrib.auth import authenticate
import jwt
from django.conf import settings
from .models import User, Blog, Like
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from .serializers import UserSerializer, PostUserSerializer, BlogSerializer, PostBlogSerializer, PostLikeSerializer, LikeSerializer

Key = settings.SECRET_KEY

# Create your views here.

class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class CreateUsers(APIView):
    def post(self, request, format=None):
        serializer = PostUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.is_active = True
            user.save()
            return Response({'response': 'User Created'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'response': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class AuthenticateUser(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            payload = {
                'user_id': user.id
            }
            token = jwt.encode(payload, Key, algorithm='HS256')
            print(token)
            
            return Response({'response': 'User Authenticated', 'token': token})
        return Response({'response': 'Invalid User Credential'}, status=status.HTTP_400_BAD_REQUEST)
        
class GetUserDetails(APIView):
    def get(self,request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except:
            return Response({'response': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user)
        return Response(serializer.data)
    

class UpdateUserDetails(APIView):
    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except:
            return Response({'response': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostUserSerializer(user, data=request.data)
        serializer.is_valid()
        print(serializer.errors)
        if serializer.is_valid():
            serializer.save()
            return Response({'response': 'User Updated'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'response': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class DeleteUser(APIView):
    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except:
            return Response({'response': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        token = request.META.get('HTTP_TOKEN')
        if token is None:
            return Response({'response': 'You Have No Access To This Blog'})
        
        payload = jwt.decode(token, Key, algorithms='HS256')
        user_token = payload.get('user_id')
        if user_id == user_token:
            user.delete()
            return Response({'response': 'User Deleted'}, status=status.HTTP_200_OK)
        else:
            return Response({'response': 'You Have No Access To Delete This User'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    

# Blog Views Strarts from here

class CreateBlog(CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = PostBlogSerializer

class ListAllBlogs(APIView):
    def get(self, request):
        queryset = Blog.objects.filter(private=False)
            
        serializer = BlogSerializer(queryset, many=True)
        for data in serializer.data:
            blog_id = data['id']
            likes = Like.objects.filter(blog=blog_id).count()
            data['Total Likes'] = likes
        return Response(serializer.data)


class GetBlogDetails(APIView):
    def get(self, request, blog):
        try:
            blog = Blog.objects.get(id=blog)
        except:
            return Response({'response': 'Blog Not Found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BlogSerializer(blog)

        token = request.META.get('HTTP_TOKEN')
        payload = jwt.decode(token, Key, algorithms='HS256')
        user = payload.get('user_id')
        print(user)
        if blog.private:
            if blog.user.id == user:
                return Response(serializer.data)
            else:
                return Response({'response': 'You Have No Access To This Blog'})
        else:
            return Response(serializer.data)

                
class UpdateBlog(APIView):
    def put(self, request, blog):
        try:
            blog = Blog.objects.get(id=blog)
        except:
            return Response({'response': 'Blog Not Found'}, status=status.HTTP_404_NOT_FOUND)
        token = request.META.get('HTTP_TOKEN')
        if token is None:
            return Response({'response': 'You Have No Access To This Blog'})
        
        payload = jwt.decode(token, Key, algorithms='HS256')
        user = payload.get('user_id')
        if blog.user.id == user:
            serializer = PostBlogSerializer(blog, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'response': 'Blog Updated'}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'response': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'response': 'You Have No Access To This Blog'})

            
class DeleteBlog(APIView):
    def delete(self,request, blog_id):
        try:
            blog = Blog.objects.get(id=blog_id)
        except:
            return Response({'response': 'Blog Not Found'}, status=status.HTTP_404_NOT_FOUND)
        token = request.META.get('HTTP_TOKEN')
        if token is None:
            return Response({'response': 'You Have No Access To This Blog'})
        
        payload = jwt.decode(token, Key, algorithms='HS256')
        user = payload.get('user_id')
        if blog.user.id == user:
            blog.delete()
            return Response({'response': 'Blog Deleted'}, status=status.HTTP_200_OK)
        else:
            return Response({'response': 'You Have No Access To This Blog'})

# Like Views Strarts from here

class LikeBlog(CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = PostLikeSerializer

class Dislike(APIView):
    def delete(self,request, blog_id):
        token = request.META.get('HTTP_TOKEN')
        if token is None:
            return Response({'response': 'You Have No Access To Dislike'})
        
        payload = jwt.decode(token, Key, algorithms='HS256')
        user_id = payload.get('user_id')
        try:
            liked_blog = Like.objects.get(blog=blog_id, user=user_id)
        except:
            return Response({'response': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        if liked_blog.user.id == user_id:
            liked_blog.delete()
            return Response({'response': 'Like Removed'}, status=status.HTTP_200_OK)
        return Response({'response': 'You Have No Access To This Blog'})
    

class GetBlogLikes(APIView):
    def get(self, request, blog_id):
        try:
            liked_blog = Like.objects.filter(blog=blog_id).count()
        except:
            return Response({'response': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        blog = Blog.objects.get(id=blog_id)
        serializer = BlogSerializer(blog)
        data = serializer.data
        data['Total Likes'] = liked_blog
        if blog.private:
            token = request.META.get('HTTP_TOKEN')
            if token is None:
                return Response({'response': 'You Have No Access To This Blog'})
            payload = jwt.decode(token, Key, algorithms='HS256')
            user = payload.get('user_id')
            print(user)
            print(blog.user.id)
            if blog.user.id == user:
                return Response(data)
            else:
                return Response({'response': 'You Have No Access To This Blog'})
        else:
            return Response(data)
        