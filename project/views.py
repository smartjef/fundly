from django.shortcuts import render, get_object_or_404
from .models import Project
from django.urls import reverse
# Create your views here.
def index(request):
    context = {
        'title': 'Projects',
        'projects': Project.objects.filter(is_active=True),
    }
    return render(request, 'projects/index.html', context)

def service_details(request, slug):
    current_project = get_object_or_404(Project, slug=slug, is_active=True)
    
    # Find the next project
    next_project = Project.objects.filter(created_at__gt=current_project.created_at, is_active=True).order_by('created_at').first()
    
    # Find the previous project
    previous_project = Project.objects.filter(created_at__lt=current_project.created_at, is_active=True).order_by('-created_at').first()
    
    context = {
        'title': current_project.title,
        'category': 'Projects',
        'category_url': reverse('project:list'),
        'next_project': next_project,
        'project': current_project,
        'previous_project': previous_project,
    }
    return render(request, 'projects/details.html', context)