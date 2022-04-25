from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from comment.models import Comment, Post


class CommentNestedSerializer(serializers.ModelSerializer):
    child_comment = SerializerMethodField(source='get_child_comment')

    class Meta:
        model = Comment
        fields = ['id', 'text', 'child_comment']

    @extend_schema_field(serializers.ListField(child=serializers.JSONField()))
    def get_child_comment(self, obj):
        depth = self.context.get('depth', 1)
        if depth < 3:
            return CommentNestedSerializer(obj.comment_set.all(),
                                           many=True,
                                           read_only=True,
                                           context={"child": obj, "depth": depth+1}).data


class PostSerializer(serializers.ModelSerializer):
    comments = SerializerMethodField(source='get_comments')

    class Meta:
        model = Post
        fields = '__all__'

    @extend_schema_field(serializers.ListField(child=CommentNestedSerializer()))
    def get_comments(self, obj):
        return CommentNestedSerializer(obj.comment_set.all(), many=True, read_only=True, context={"comment": obj}).data


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

    def validate(self, data):
        parent_comment = data.get('parent_comment')
        if parent_comment:
            try:
                post_id = Comment.objects.get(pk=parent_comment.pk).post_id
            except Comment.DoesNotExist:
                raise ValidationError('there is no this parent comment in database')
            input_post_id = data.get('post')
            if str(post_id) != str(input_post_id.pk):
                raise ValidationError('this parent comment is not attached to this post ')
        return data
