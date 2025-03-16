from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('', views.my_profile, name='profile'),
    path('add-image/', views.update_profile_pic, name='update_pic'),
    path('team/', views.team, name='team'),
    path('team/<slug:slug>/', views.team_details, name='team_details')
]
