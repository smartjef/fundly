from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('docs/', views.docs, name='docs'),
    path('testimonies/', views.testimonies, name='testimonies'),
    path('add-review/', views.review, name='review'),
    path('faqs/', views.faq, name='faq'),
    path('search/', views.search, name='search'),
    path('terms-and-conditions/', views.terms, name='terms'),
    path('privacy-policy/', views.policy, name='policy'),
]
