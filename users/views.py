from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Team, Profile, Preferences
from project.models import Project
import re
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def validate_username(username):
    regex = '^[a-zA-Z0-9]+$'
    if not re.match(regex, username):
        return False
    return True

# Create your views here.
def team(request):
    context = {
        'title': 'Team Members',
        'team': Team.objects.filter(is_active=True),
    }
    return render(request, 'users/team/index.html', context)

def team_details(request, slug):
    team = get_object_or_404(Team, slug=slug, is_active=True)
    if team.user.get_full_name():
        title = team.user.get_full_name()
    else:
        title = "No Name Provided"
    context = {
        'team': team,
        'title': title,
        'category': 'Team',
        'category_url': reverse('users:team'),
        'projects': Project.objects.filter(is_active=True),
    }
    return render(request, 'users/team/details.html', context)

@login_required
def my_profile(request):

    user = request.user
    profile = get_object_or_404(Profile, user=user, user__is_active=True)
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        #social accounts
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        twitter = request.POST.get('twitter')
        linkedin = request.POST.get('linkedin')
        #preferences
        language = request.POST.get('language')
        theme = request.POST.get('theme')
        if not validate_username(username):
            messages.warning(request, 'Username can only contain letters and numbers.')
            return redirect('users:profile')
        else:
            #validate username to confirm it doesnt already exist
            if User.objects.filter(username=username).exists() and username != user.username:
                messages.warning(request, 'Username already exists.')
                return redirect('users:profile')
            else:
                #user
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()
                #profile
                profile.phone_number = phone_number
                profile.gender = gender
                profile.facebook = facebook
                profile.instagram = instagram
                profile.twitter = twitter
                profile.linkedin = linkedin
                profile.save()
                #preference
                preferences = Preferences.objects.get(user=user)
                preferences.language = language
                preferences.theme = theme
                preferences.save()
                messages.success(request, 'Profile updated successfully.')
    context = {
        'title': 'Profile',
        'category': 'Accounts',
    }
    return render(request, 'users/profile.html', context)

@login_required
@require_POST
def update_profile_pic(request):
    user = request.user
    if request.method == 'POST':
        profile = get_object_or_404(Profile, user=user, user__is_active=True)
        image = request.FILES.get('image', None)
        if image:
            profile.image = image
            profile.save()
            messages.success(request, 'Profile Picture changed successfully.')
    return redirect('users:profile')