from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('about', views.AboutViewSet, basename='about')
router.register('services', views.ServiceViewSet, basename='service')
# router.register('services/(?P<service_pk>\d+)/faqs', views.ServiceFAQViewSet, basename='service-faq')
router.register('posts', views.PostViewSet, basename='post')
# router.register('posts/(?P<post_pk>\d+)/comments', views.PostCommentViewSet, basename='post-comment')
# router.register('comments/(?P<comment_pk>\d+)/replies', views.CommentReplyViewSet, basename='comment-reply')
router.register('team', views.TeamViewSet, basename='team')
router.register('tags', views.TagViewSet, basename='tag')
# router.register('tags/(?P<tag_pk>\d+)/posts', views.TagPostViewSet, basename='tag-post')
router.register('categories', views.CategoryViewSet, basename='category')
# router.register('categories/(?P<category_pk>\d+)/posts', views.CategoryPostViewSet, basename='category-post')
router.register('projects', views.ProjectViewSet, basename='project')
router.register('testimonies', views.TestimonyViewSet, basename='testimony')
router.register('faqs', views.FAQViewSet, basename='faq')
router.register('partners', views.PartnerViewSet, basename='partner')
router.register('contacts', views.ContactCreateViewSet, basename='contact')

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]