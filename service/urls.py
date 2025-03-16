from django.urls import path
from . import views

app_name = 'services'
urlpatterns = [
    path('', views.index, name='list'),
    path('<slug:slug>/', views.service_details, name='detail'),
]