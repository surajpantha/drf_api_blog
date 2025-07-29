from rest_framework import serializers
from .models import CustomUser,Blog

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['id','email','username','first_name','last_name','bio','profile_picture','facebook','youtube','instagram']
        extra_kwargs = {
            'password': {'write_only': True}  # don't return password in API responses
        }


    def create(self,validated_data):
         password = validated_data.pop('password')  
         user = CustomUser(**validated_data)        
         user.set_password(password)                
         user.save()
         return user
    
class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['id','email','username','first_name','last_name','password']
    
class SimpleAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['id','username','first_name','last_name']


class BlogSerializer(serializers.ModelSerializer):
    author=SimpleAuthorSerializer(read_only=True)
    class Meta:
        model=Blog
        fields=['id', 'title', 'slug', 'author', 'category', 'content', 'featured_image', 'published_at', 'created_at', 'updated_at', 'is_draft']

    def validate_featured_image(self, value):
        max_size = 5 * 1024 * 1024  # 5MB
        if value and value.size > max_size:
            raise serializers.ValidationError("Image too large")
        return value




