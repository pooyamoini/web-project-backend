from rest_framework import serializers
from .models import Comment

<<<<<<< Updated upstream
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Comment
        fields = '__all__'
=======

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
>>>>>>> Stashed changes
