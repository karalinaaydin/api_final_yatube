from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model

from posts.models import Comment, Post, Group, Follow

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username'
    )

    class Meta:
        model = Follow
        fields = '__all__'

    def validate_following(self, value):
        """Пользователь не может подписаться на самого себя."""
        request_user = self.context.get('request').user
        if request_user == value:
            raise serializers.ValidationError(
                "Вы не можете подписаться на самого себя."
            )
        if Follow.objects.filter(user=request_user, following=value).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого пользователя."
            )
        return value
