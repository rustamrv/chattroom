from rest_framework import serializers
from feed.models import Post
from accounts.models import Profile


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ("email", "first_name", "last_name")

class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    recipient = UserSerializer()

    class Meta:
        model =  Post
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    recipient = UserSerializer()

    class Meta:
        model =  Post
        fields = '__all__'
