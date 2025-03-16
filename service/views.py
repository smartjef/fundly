from django.shortcuts import render, get_object_or_404, redirect
from .models import Service
from django.urls import reverse
# Create your views here.
def index(request):
    context = {
        'title': 'Our Services',
        'services': Service.objects.all(),
    }
    return render(request, 'services/index.html', context)

def service_details(request, slug):
    service = get_object_or_404(Service, slug=slug)
    context = {
        'title': service.title,
        'category': 'services',
        'category_url': reverse('services:list'),
        'service': service,
        'services': Service.objects.all(),
    }
    return render(request, 'services/details.html', context)