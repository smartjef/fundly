from django.contrib.sitemaps import Sitemap

from .models import Team


class TeamSitemap(Sitemap):
    changefreq = 'always'
    priority = 0.9

    def items(self):
        return Team.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return obj.get_absolute_url()
    