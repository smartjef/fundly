from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, PostLike
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Tag, Category
from django.urls import reverse
from django.db import IntegrityError
from django.views.decorators.http import require_POST
# Create your views here.
def index(request, category_slug=None, tag_slug=None):
    blogs = Post.objects.filter(is_published=True)
    query = request.GET.get('q')
    title = 'Blogs'
    #filter by category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        blogs = Post.objects.filter(is_published=True, category=category)
        title = f"Blogs under category, { category }"

    #filter by search
    if query:
        blogs = Post.objects.filter(is_published=True, title__icontains=query) or Post.objects.filter(is_published=True, body__icontains=query)
        number_of_blogs = blogs.count()
        title = f"{number_of_blogs} Blogs matchets the query, {query}"

    #filter by tag
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        blogs = Post.objects.filter(is_published=True, tags=tag)
        title = f"Blogs with tag, { tag }"

    context = {
        'title': title,
        'blogs': blogs,
        'latest_posts': blogs[:5],
        'categories': Category.objects.all()[:5],
        'tags': Tag.objects.all()[:6],
        'recent_comments': Comment.objects.filter(is_approved=True)
    }
    return render(request, 'blog/index.html', context)

def blog_detail(request, slug, id=None):
    comment=None
    post = get_object_or_404(Post, slug=slug, is_published=True)
    post.views += 1
    post.save()

    next_post = Post.objects.filter(created_at__gt=post.created_at, is_published=True, author=post.author).order_by('created_at').first()
    previous_post = Post.objects.filter(created_at__lt=post.created_at, is_published=True, author=post.author).order_by('created_at').first()
    if id:
        comment =  get_object_or_404(Comment, id=id)

    blog_full_url = f"{request.scheme}://{request.get_host()}{post.get_absolute_url()}"
    context = {
        'title': post.title,
        'category_url': reverse('blog:list'),
        'category': f'Blogs > { post.category }',
        'post': post,
        'next_post': next_post,
        'previous_post': previous_post,
        'tags': Tag.objects.all()[:6],
        'categories': Category.objects.all()[:5],
        'comment': comment,
        'latest_posts': Post.objects.filter(is_published=True)[:5],
        'recent_comments': Comment.objects.filter(is_approved=True),
        'blog_full_url': blog_full_url,
        'blog_text': f"Checkout this blog, {post.title} by {post.author.get_full_name()} on Fundly Limited"
    }
    return render(request, 'blog/details.html', context)

@login_required
@require_POST
def comment(request, slug, id=None):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    if request.method == 'POST':
        message = request.POST.get('message')
        if id:
            comment = get_object_or_404(Comment, id=id)
            comment.message = message
            comment.save()
            messages.success(request, 'Comment modified successfully')
        else:
            if message and request.user.is_authenticated:
                new_message = Comment.objects.create(post=post, author=request.user, message=message)
                new_message.save()
                messages.success(request, 'Comment left successfully')
            else:
                messages.warning(request, 'Message cant be blank')
    return redirect('blog:detail', slug=slug)
        
@login_required
def edit_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    if request.user != comment.author:
        messages.warning(request, 'You are not authorized to modify this comment')
    else:
        return redirect('blog:detail', comment.post.slug, comment.id)
    return redirect('blog:detail', comment.post.slug )

@login_required
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    if request.user != comment.author:
        messages.warning(request, 'You are not authorized to delete this comment')
    else:
        comment.delete()
        messages.success(request, 'Comment successfully deleted!')
    return redirect('blog:detail', comment.post.slug )


@login_required
def like_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    try:
        like, created = PostLike.objects.get_or_create(user=request.user, post=post, value='like')
        if not created:
            # User already liked this answer
            messages.warning(request, "You already liked this post")
        else:
            post.increase_likes()
            messages.success(request, "Post liked!")
    except IntegrityError:
        like = PostLike.objects.get(user=request.user, post=post)
        if like.value == 'like':
            messages.warning(request, "You already liked this post")
        else:
            like.value = 'like'
            like.save()
            post.increase_likes()
            post.decrease_dislikes()
            messages.success(request, "Post liked!")

    return redirect('blog:detail', slug=post.slug)

@login_required
def dislike_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    try:
        like, created = PostLike.objects.get_or_create(user=request.user, post=post, value='dislike')
        if not created:
            # User already disliked this answer
            messages.warning(request, "You already disliked this post")
        else:
            post.increase_dislikes()
            messages.success(request, "Post disliked!")
    except IntegrityError:
        like = PostLike.objects.get(user=request.user, post=post)
        if like.value == 'dislike':
            messages.warning(request, "You already disliked this post")
        else:
            like.value = 'dislike'
            like.save()
            post.increase_dislikes()
            post.decrease_likes()
            messages.success(request, "Post disliked!")

    return redirect('blog:detail', slug=post.slug)
