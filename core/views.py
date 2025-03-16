from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from service.models import Service
from project.models import Project
from blog.models import Post
from .models import Testimony, Partner, FAQ, Contact
from users.models import Team
from django.views.decorators.http import require_POST

def check_if_userprofile_is_updated(user):
    if user.first_name and user.last_name and user.email:
        return True
    else:
        return False
    
# Create your views here.
def index(request):
    context = {
        'title' : 'Homepage',
        'services': Service.objects.all()[:4],
        'projects': Project.objects.filter(is_active=True),
        'testimonies': Testimony.objects.filter(is_active=True)[:3],
        'partners': Partner.objects.all(),
        'faqs': FAQ.objects.filter(is_active=True)[:2],
        'blogs': Post.objects.filter(is_published=True)[:3],
    }
    return render(request, f'index.html', context)

def contact(request):
    if request.method == "POST":
        name = request.POST.get('full_name')
        email = request.POST.get('user_email')
        subject = request.POST.get('subject')
        if subject:
            subject = subject
        else:
            subject = 'Contact by ' + name + ' - ' + email + ' - ' + 'No Subject'
        message = request.POST.get('message')
        if message:
            message = message
        else:
            message = "No Message in the body"

        phone_number = request.POST.get('phone')
        contact = Contact(name=name, email=email, subject=subject, message=message, phone_number=phone_number)
        contact.save()
        messages.success(request, 'Contact request submitted successfully.')
        return redirect('index')

    context = {
        'title': 'Contact Us'
    }
    return render(request, 'contact.html', context)

def about(request):
    context = {
        'title': 'About Us',
        'partners': Partner.objects.all(),
        'projects': Project.objects.filter(is_active=True),
    }
    return render(request, 'about.html', context)

@login_required
@require_POST
def review(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        position = request.POST.get('position')
        message = request.POST.get('message')
        new_testimony =Testimony.objects.create(author=request.user, rating=rating, position=position, message=message)
        new_testimony.save()
        messages.success(request, 'Review added successfully.')
    return redirect('testimonies')

def testimonies(request):
    context = {
        'title': 'Testimonies',
        'testimonies': Testimony.objects.filter(is_active=True),
    }
    return render(request, 'testimonial.html', context)

def faq(request):
    context = {
        'title': 'FAQs',
        'faqs': FAQ.objects.filter(is_active=True),
    }
    return render(request, 'faq.html', context)

def search(request):
    query = request.GET.get('q')
    title = 'Search page'

    blogs = None
    testimonies = None 
    services = None
    projects = None
    faqs = None
    teams = None

    if query:
        blogs = Post.objects.filter(is_published=True, title__icontains=query) or Post.objects.filter(is_published=True, body__icontains=query)
        testimonies = Testimony.objects.filter(is_active=True, message__icontains=query) or Testimony.objects.filter(is_active=True, author__first_name__icontains=query)
        services = Service.objects.filter(title__icontains=query) or Service.objects.filter(description__icontains=query)
        projects = Project.objects.filter(is_active=True, title__icontains=query) or Project.objects.filter(is_active=True, description__icontains=query)
        faqs = FAQ.objects.filter(is_active=True, question__icontains=query) or FAQ.objects.filter(is_active=True, answer__icontains=query)
        teams = Team.objects.filter(is_active=True, user__first_name__icontains=query) or Team.objects.filter(is_active=True, rank__icontains=query)
        total_results = blogs.count()+testimonies.count()+services.count()+projects.count()+faqs.count()+teams.count()
        title = f"{total_results} Search result for '{query}'"
    context = {
        'title': title,
        'blogs': blogs,
        'testimonies': testimonies,
        'services': services,
        'projects': projects,
        'faqs': faqs,
        'teams': teams,
    }
    return render(request, 'search.html', context)

def policy(request):
    context = {
        'title': 'Privacy Policy',   
    }
    return render(request, 'policy.html', context)

def terms(request):
    context = {
        'title': 'Terms & Conditions',   
    }
    return render(request, 'terms.html', context)

def docs(request):
    context = {
        'title': 'Documentation',
    }
    return render(request, 'docs.html', context)