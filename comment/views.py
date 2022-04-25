from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from comment.models import Comment, Post
from comment.serializers import CommentNestedSerializer, CommentSerializer, PostSerializer


@extend_schema_view(
    list=extend_schema(
        description='return all posts with comments, including nested comments through 3 level'))
class PostListView(GenericViewSet, ListModelMixin):
    queryset = Post.objects.all().prefetch_related(Prefetch(
        'comment_set',
        queryset=Comment.objects.filter(parent_comment_id__isnull=True)))
    serializer_class = PostSerializer


@extend_schema_view(
    retrieve=extend_schema(
        description='return post via id with comments, including nested comments through 3 level'),
    destroy=extend_schema(
        description='delete one post with all nested comments'),
    create=extend_schema(
        description='create post'),
)
class PostView(GenericViewSet, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = Post.objects.all().prefetch_related(Prefetch(
        'comment_set',
        queryset=Comment.objects.filter(parent_comment_id__isnull=True)))
    serializer_class = PostSerializer


@extend_schema_view(
    retrieve=extend_schema(
        description='return comment via id, including nested comments through 3 level'),
    destroy=extend_schema(
        description='delete one comment with all nested comments'),
    create=extend_schema(
        description='create comment'),
)
class CommentView(GenericViewSet, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin):
    queryset = Comment.objects.all()
    http_method_names = ['get', 'post', 'head', 'options', 'delete']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            serializer_class = CommentNestedSerializer
        else:
            serializer_class = CommentSerializer
        return serializer_class
