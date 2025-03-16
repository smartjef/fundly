from django.db import models
from django.urls import reverse
# Create your models here.
class About(models.Model):
    title = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    
    #social media
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    
    #address
    address = models.CharField(blank=True, null=True, max_length=256)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_addressed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class Testimony(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    
    class Meta:
        ordering = ('-rating',)

class Partner(models.Model):
    title = models.CharField(max_length=100)
    website = models.URLField(max_length=200, blank=True, null=True)
    logo = models.ImageField(upload_to='Partners/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-created_at',)

class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
    
    class Meta:
        ordering = ('-created_at',)

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150)

    def __str__(self):
        return self.title

class Tag(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150)

    def __str__(self):
        return self.title
    