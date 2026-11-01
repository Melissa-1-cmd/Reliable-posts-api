from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):

    author= serializers.StringRelatedField(read_only=True)

    class Meta:
        model=Post
        fields=['id','title','content','author','created_at']

        read_only_fields=['id','author','created_at']