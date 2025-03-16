from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from service.models import Service, ServiceFAQ
from core.models import About, FAQ, Partner, Testimony, Tag, Category, Contact
from users.models import Team
from blog.models import Post, Comment, Reply
from project.models import Project
from .serializers import ServiceSerializer, AboutSerializer, FAQSerializer, PartnerSerializer, TestimonySerializer, PostSerializer, ProjectSerializer, ServiceFAQSerializer, TeamSerializer, CommentSerializer, ReplySerializer, TagSerializer, CategorySerializer, ContactSerializer
# Create your views here.

class IsObjOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
    
class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceFAQViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ServiceFAQSerializer

    def get_queryset(self):
        service_pk = self.kwargs.get('service_pk')
        service = get_object_or_404(Service, pk=service_pk)
        queryset = ServiceFAQ.objects.filter(service=service)
        return queryset

class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.filter(is_active=True)
    serializer_class = TeamSerializer

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer

class PostCommentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_pk, is_published=True)
        queryset = Comment.objects.filter(post=post, is_approved=True)
        return queryset
    
class CommentReplyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReplySerializer

    def get_queryset(self):
        comment_pk = self.kwargs.get('comment_pk')
        comment = get_object_or_404(Comment, pk=comment_pk, is_approved=True)
        queryset = Reply.objects.filter(comment=comment, is_approved=True)
        return queryset
    
class AboutViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = About.objects.filter(is_active=True)
    serializer_class = AboutSerializer

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagPostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        tag_pk = self.kwargs.get('tag_pk')
        tag = get_object_or_404(Tag, pk=tag_pk)
        queryset = Post.objects.filter(tags=tag, is_published=True)
        return queryset
    
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryPostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        category_pk = self.kwargs.get('category_pk')
        category = get_object_or_404(Category, pk=category_pk)
        queryset = Post.objects.filter(category=category, is_published=True)
        return queryset

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.filter(is_active=True)
    serializer_class = ProjectSerializer

class TestimonyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Testimony.objects.filter(is_active=True)
    serializer_class = TestimonySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

        serializer = TestimonySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = FAQSerializer

class PartnerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

class ContactCreateViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.none()

    def create(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

