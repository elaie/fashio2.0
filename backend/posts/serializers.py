from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id','post_name','post_bio', 'post_likes', 'post_comment', 'post_image',]