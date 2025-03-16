
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from project.sitemaps import ProjectSitemap
from service.sitemaps import ServiceSitemap
from users.sitemaps import TeamSitemap

sitemaps = {
    'posts': PostSitemap,
    'services': ServiceSitemap,
    'projects': ProjectSitemap,
    'team': TeamSitemap,
}

urlpatterns = [
    path('', include('core.urls')),
    path('accounts/', include('allauth.urls')),
    path('v-s/', admin.site.urls),
    path('blogs/', include('blog.urls')),
    path('projects/', include('project.urls')),
    path('services/', include('service.urls')),
    path('users/', include('users.urls')),
    path('funds/', include('mchango.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitempas.views.sitemap'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Fundly Admin'
admin.site.site_title = 'Fundly Admin'
