from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


LIKE_CHOICES = (
    ('like', 'Like'),
    ('dislike', 'Dislike'),
)
#Model for Blog
class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ForeignKey('core.Category', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    body = models.TextField()
    tags = models.ManyToManyField('core.Tag', blank=True)
    front_image = models.ImageField(upload_to='blogs/front/images/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='blogs/cover/images/', null=True, blank=True)
    is_published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    published_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def increase_likes(self):
        self.likes += 1
        self.save()

    def decrease_likes(self):
        self.likes -= 1
        self.save()

    def increase_dislikes(self):
        self.dislikes += 1
        self.save()

    def decrease_dislikes(self):
        self.dislikes -= 1
        self.save()


    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})
    
    class Meta:
        ordering = ('-created_at',)
        
class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=10)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} {self.value} {self.post}"
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

    class Meta:
        ordering = ('-created_at',)

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Reply by {self.author} on {self.comment}'

    class Meta:
        ordering = ('-created_at',)