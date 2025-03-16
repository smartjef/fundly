from django.contrib import admin
from .models import Project
# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'website', 'client', 'is_active', 'updated_at')
    list_filter = ('created_at','category', 'updated_at')
    search_fields = ('title', 'slug', 'category', 'description', 'client', 'website')
    date_hierarchy = 'created_at'
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at','updated_at')
    list_per_page = 20
    autocomplete_fields = ['category', ]
    actions = ['mark_as_active', 'mark_as_inactive']

    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, 'Selected projects have been marked as active')

    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, 'Selected projects have been marked as inactive')

