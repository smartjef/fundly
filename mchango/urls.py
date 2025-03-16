from django.urls import path
from . import views

app_name = 'mchango'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<slug:slug>/', views.contribute, name='contribute'),
    path('<int:pk>/d/<slug:slug>/', views.dashboard, name='dashboard'),
    path('<int:pk>/e/<slug:slug>/', views.edit, name='edit'),
    path('<int:pk>/s/<slug:slug>/', views.change_status, name='change_status'),
    path('<int:pk>/c/<slug:slug>/', views.close, name='close'),
    path('p/<slug:slug>/', views.store_pledge, name='store_pledge'),
]
