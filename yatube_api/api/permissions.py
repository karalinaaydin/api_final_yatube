from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Разрешает доступ только автору.

    Автор может редактировать и удалять свои посты и комментарии.
    Остальным пользователям разрешает доступ только на чтение.
    """

    def has_object_permission(self, request, view, instance):
        return (request.method in permissions.SAFE_METHODS
                or instance.author == request.user)
