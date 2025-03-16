from django.contrib import admin
from .models import Service, ServiceFAQ
# Register your models here.

class ServiceFAQInline(admin.TabularInline):
    model = ServiceFAQ
    extra = 0
    show_change_link = True
    fields = ('question', 'answer', 'is_active', 'created_at')
    readonly_fields = ('updated_at', 'created_at')
    ordering = ('-created_at',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'slug', 'created_at', 'updated_at']
    search_fields = ['title', 'description', 'slug']
    list_filter = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20
    ordering = ['-created_at',]
    inlines = [ServiceFAQInline]