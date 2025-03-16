from rest_framework import serializers
from service.models import Service, ServiceFAQ
from core.models import About, Partner, FAQ, Testimony, Tag, Category, Contact
from django.contrib.auth.models import User
from users.models import Profile, Team
from blog.models import Post, Comment, Reply
from project.models import Project

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'slug'] 

class ProjectSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    class Meta:
        model = Project
        fields = ['title', 'slug', 'category', 'front_image', 'cover_image', 'description', 'website', 'client', 'date_completed',  'created_at'] 

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title', 'slug'] 

class ServiceFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceFAQ
        fields = ['id', 'question', 'answer',  'created_at'] 

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['title', 'description', 'front_image', 'cover_image']

class ServiceFaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceFAQ
        fields = ['question', 'answer',  'created_at']

class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ['title', 'phone_number', 'email', 'twitter', 'facebook', 'linkedin', 'youtube', 'github', 'address', 'created_at']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image',]

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, read_only=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile']

class TeamSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Team
        fields = ['user', 'rank', 'image', 'created_at'] 

class TestimonySerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Testimony
        fields = ['position', 'message', 'rating',  'created_at', 'author']

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['title', 'website', 'logo', 'created_at']

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['question', 'answer',  'created_at']

class ReplySerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Reply
        fields = ['author', 'message', 'created_at']  

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Comment
        fields = ['author', 'message', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['title', 'slug', 'category', 'author', 'body', 'tags', 'front_image', 'cover_image', 'views', 'likes', 'dislikes', 'created_at']
   
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
