from django.shortcuts import render
from .serializers import UserRegistrationSerializer,BlogSerializer,UpdateUserProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Blog
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse

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


@api_view(['POST'])
@permission_classes([IsAuthenticated])

def delete_blog(request,pk):
  user=request.user
  blog=get_object_or_404(Blog,id=pk,author=user)
  blog.delete()
  return Response({'message:blog deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


def create_admin_user(request):
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "adminpassword")
        return JsonResponse({"message": "Superuser created"})
    return JsonResponse({"message": "Superuser already exists"})