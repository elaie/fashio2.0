from .models import StripeModel, BillingAddress, OrderModel, User, Tweet, TweetLike, UserFollower
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken



class UserSerializer(serializers.ModelSerializer):
    admin = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'display_name', 'email', 'password', 'verified', 'photo', 'header_photo', 'bio', 'birth_date', 'location', 'website', 'date_joined',"admin")

        def get_admin(self, obj):
            return obj.is_staff
        
class UserRegisterTokenSerializer(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'display_name', 'email', 'password', 'verified', 'photo', 'header_photo', 'bio', 'birth_date', 'location', 'website', 'date_joined',"admin", "token"]

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    def get_admin(self, obj):
            return obj.is_staff



class TweetUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Tweet
        fields = ('id', 'user', 'text', 'image', 'created_at', 'updated_at')

class TweetWithoutUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ('id', 'text', 'image', 'created_at', 'updated_at')

class TweetLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetLike
        fields = ('id', 'user', 'tweet', 'created_at')

class TweetLikeExposeTweetSerializer(serializers.ModelSerializer):
    tweet = TweetUserSerializer()
    class Meta:
        model = TweetLike
        fields = ('id', 'user', 'tweet', 'created_at')

class TweetLikeWithoutUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        tweet_like, created = TweetLike.objects.get_or_create(**validated_data)
        return tweet_like
    class Meta:
        model = TweetLike
        fields = ('id', 'tweet', 'created_at')

class UserFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollower
        fields = ('id', 'user', 'follower', 'created_at')

class UserFollowerWithoutFollowerSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user_follower, created = UserFollower.objects.get_or_create(**validated_data)
        return user_follower
    class Meta:
        model = TweetLike
        fields = ('id', 'user', 'created_at')

class UserFollowerExposeUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserFollower
        fields = ('id', 'user', 'follower', 'created_at')

class UserFollowerExposeFollowerSerializer(serializers.ModelSerializer):
    follower = UserSerializer()
    class Meta:
        model = UserFollower
        fields = ('id', 'user', 'follower', 'created_at')

# creating tokens manually (with user registration we will also create tokens)

# list of cards
class CardsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = StripeModel
        fields = "__all__"


# billing address details
class BillingAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingAddress
        fields = "__all__"


# all orders list
class AllOrdersListSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderModel
        fields = "__all__"