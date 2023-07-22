from rest_framework import serializers
from .models import User, Blog, Like


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Blog
        fields = '__all__'

class PostBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    blog = BlogSerializer()
    class Meta:
        model = Like
        fields = '__all__'

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

