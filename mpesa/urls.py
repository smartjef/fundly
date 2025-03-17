from django.urls import path
from . import views

app_name = 'mpesa'
urlpatterns = [
    path('b2c/result/', views.b2c_result, name='b2c_result'),
    path('c2b/result/', views.c2b_confirm, name='c2b_result'),
]