from django.contrib import admin
from .models import Post, Comment, Reply, PostLike
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'author', 'views', 'likes', 'dislikes', 'is_published', 'published_date', 'created_at', 'updated_at')
    list_filter = ('category', 'author', 'is_published', 'published_date', 'created_at', 'updated_at')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)
    autocomplete_fields = ['category', 'author', 'tags']
    filter_vertical = ['tags',]
    list_per_page = 10

class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 0
    can_delete = False
    show_change_link = True
    fields = ('author', 'message', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    autocomplete_fields = ['author']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'is_approved', 'created_at', 'updated_at')
    list_filter = ('is_approved', 'created_at', 'updated_at')
    search_fields = ('author', 'message')
    date_hierarchy = 'created_at'
    autocomplete_fields = ['post', 'author']
    ordering = ('-created_at',)
    inlines = [ReplyInline]
    list_per_page = 20

@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'value')
    search_fields = ('post', 'user')
    autocomplete_fields = ['post', 'user']
    list_per_page = 20