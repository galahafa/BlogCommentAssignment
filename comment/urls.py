from django.urls import include, path
from rest_framework import routers

from comment.views import CommentView, PostListView, PostView

router = routers.DefaultRouter()
router.register('posts', PostListView, basename='posts')
router.register('post', PostView, basename='post')
router.register('comment', CommentView, basename='comment')

urlpatterns = [path('', include(router.urls))]
