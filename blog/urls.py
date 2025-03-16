from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='list'),
    path('category/<slug:category_slug>/', views.index, name='list_by_category'),
    path('tags/<slug:tag_slug>/', views.index, name='list_by_tag'),
    path('<slug:slug>/', views.blog_detail, name='detail'),
    path('<slug:post_slug>/like/', views.like_post, name='like_post'),
    path('<slug:post_slug>/dislike/', views.dislike_post, name='dislike_post'),
    path('<slug:slug>/<int:id>/', views.blog_detail, name='detail'),
    path('<slug:slug>/comment/', views.comment, name='comment'),
    path('<slug:slug>/comment/<int:id>/', views.comment, name='comment'),
    path('comment/<int:id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:id>/delete/', views.delete_comment, name='delete_comment'),
]
