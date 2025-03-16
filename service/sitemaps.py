from django.contrib.sitemaps import Sitemap

from .models import Service


class ServiceSitemap(Sitemap):
    changefreq = 'always'
    priority = 0.9

    def items(self):
        return Service.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return obj.get_absolute_url()