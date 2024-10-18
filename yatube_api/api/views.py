from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter

from posts.models import Group, Post, Follow
from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer, FollowSerializer


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели Group (только для чтения)."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_post(self):
        """Возвращаем объект поста по параметру post_pk."""
        return get_object_or_404(Post, id=self.kwargs.get('post_pk'))

    def get_queryset(self):
        """Фильтруем комментарии по post_id из URL."""
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        """Создаём комментарий, добавляя автора и пост."""
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Возвращает все подписки для залогиненного пользователя."""
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Создает новую подписку."""
        serializer.save(user=self.request.user)
