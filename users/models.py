from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from main.settings import LANGUAGES as LANGUAGE_CHOICES, THEME_CHOICES  

# Create your models here.

GENDER_CHOICES = (
    ('male', 'male'),
    ('female', 'female'),
    ('other', 'other')
)


class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')
    image = models.ImageField(upload_to='users/profiles/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_hidden_phone(self):
        phone = self.phone_number
        if phone.startswith('254'):
            return f"{phone[:4]}XX XXX {phone[-3:]}"
        elif phone.startswith('0'):
            return f"254{phone[1:3]} XX {phone[-3:]}"
        else:
            return phone

class Team(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='team')
    slug = models.SlugField(unique=True)
    rank = models.CharField(max_length=100)
    image = models.ImageField(upload_to='users/teams/')
    experience = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ('order',)
    
    def get_absolute_url(self):
        return reverse('users:team_details', kwargs={'slug': self.slug})
    
class Skill(models.Model):
    team_member = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="skills")
    title = models.CharField(max_length=100)
    level = models.PositiveSmallIntegerField(default=0, help_text="In percentage, e.g 90")

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-level',)

class Project(models.Model):
    user = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='projects')
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='teams')
    role = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.project.title}"
    
    class Meta:
        ordering = ('-project__created_at',)

class Preferences(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='preferences')
    language = models.CharField(max_length=100, choices=LANGUAGE_CHOICES, default='en')
    theme = models.CharField(max_length=100, choices=THEME_CHOICES, default='light')

    def __str__(self):
        return f"{self.user.username}'s Preferences"
    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,)
        Preferences.objects.create(user=instance,)