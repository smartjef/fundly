from django.db import models
from django.urls import reverse
from django.utils import timezone
# Create your models here.

    
class Project(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150)
    category = models.ForeignKey('core.Category', on_delete=models.CASCADE, related_name='projects')
    front_image = models.ImageField(upload_to='projects/front/')
    cover_image = models.ImageField(upload_to='projects/cover/')
    description = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    client = models.CharField(max_length=200, null=True, blank=True)
    date_completed = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_status(self):
        if self.date_completed:
            if self.date_completed > timezone.now().date():
                return 'Upcoming'
            return 'Completed'
        return 'Ongoing'
    
    def get_absolute_url(self):
        return reverse('project:detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('-created_at',)

        
