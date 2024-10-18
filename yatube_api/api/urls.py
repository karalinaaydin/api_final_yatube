from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('posts', views.PostViewSet)
router.register(
    r'posts/(?P<post_pk>\d+)/comments',
    views.CommentViewSet, basename='comment'
)
router.register(r'groups', views.GroupViewSet, basename='group')
router.register(r'follow', views.FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router.urls)),
]
