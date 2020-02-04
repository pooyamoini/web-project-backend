from rest_framework import serializers
from .models import Comment, SubComment, RowComment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class RowCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RowComment
        fields = '__all__'


class SubCommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = SubComment
        fields = '__all__'
