from django.shortcuts import render
from .serializers import UserRegistrationSerializer,BlogSerializer,UpdateUserProfileSerializer,UserInfoSerializer,SimpleAuthorSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Blog
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

# Create your views here.

@api_view(['POST'])
def register_user(request):
  serializer=UserRegistrationSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data)
  return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_userprofile(request):
  user =request.user
  serializer=UpdateUserProfileSerializer(user,data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data)
  return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_blog(request):
  user=request.user
  serializer=BlogSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save(author=user)
    return Response(serializer.data)
  return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def blog_list(request):
  blogs=Blog.objects.all()
  serializer=BlogSerializer(blogs,many=True)
  return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_blog(request,pk):
  user=request.user

  blog=get_object_or_404(Blog,id=pk,author=user)
 
  serializer=BlogSerializer(blog,data=request.data,partial=True)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data)
  return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])

def delete_blog(request,pk):
  user=request.user
  blog=get_object_or_404(Blog,id=pk,author=user)
  blog.delete()
  return Response({'message:blog deleted successfully'}, status=status.HTTP_204_NO_CONTENT)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_username(request):
    user = request.user
    username = user.username
    return Response({"username": username})


@api_view(['GET'])
def get_userinfo(request, username):
    User = get_user_model()
    user = User.objects.get(username=username)
    serializer = UserInfoSerializer(user)
    return Response(serializer.data)


@api_view(["GET"])
def get_user(request, email):
    User = get_user_model()
    try:
        existing_user = User.objects.get(email=email)
        serializer = SimpleAuthorSerializer(existing_user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    


