from django.contrib.auth import authenticate, login, logout
from .models import StripeModel, BillingAddress, OrderModel
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import authentication, permissions
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from rest_framework_simplejwt.views import TokenObtainPairView # for login page
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from .serializers import (
    UserSerializer, 
    UserRegisterTokenSerializer, 
    CardsListSerializer, 
    BillingAddressSerializer,
    AllOrdersListSerializer
)
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator

from .models import User, Tweet, TweetLike, UserFollower
from .serializers import (
    TweetUserSerializer, TweetLikeExposeTweetSerializer, TweetWithoutUserSerializer, 
    TweetLikeSerializer, TweetLikeWithoutUserSerializer, 
    UserFollowerSerializer, UserFollowerWithoutFollowerSerializer, UserFollowerExposeUserSerializer, UserFollowerExposeFollowerSerializer,
)
from .exceptions import CannotFollowSelfError, CannotActionOtherUserInfoError
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

# register user
class UserRegisterView(APIView):
    """To Register the User"""

    def post(self, request, format=None):
        data = request.data # holds username and password (in dictionary)
        username = data["username"]
        email = data["email"]

        if username == "" or email == "":
            return Response({"detial": "username or email cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            check_username = User.objects.filter(username=username).count()
            check_email =  User.objects.filter(email=email).count()

            if check_username:
                message = "A user with that username already exist!"
                return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
            if check_email:
                message = "A user with that email address already exist!"
                return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
            else:
                user = User.objects.create(
                    username=username,
                    email=email,
                    password=make_password(data["password"]),
                )
                serializer = UserRegisterTokenSerializer(user, many=False)
                return Response(serializer.data)

# login user (customizing it so that we can see fields like username, email etc as a response 
# from server, otherwise it will only provide access and refresh token)
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserRegisterTokenSerializer(self.user).data

        for k, v in serializer.items():
            data[k] = v
        
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# list all the cards (of currently logged in user only)
class CardsListView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # show stripe cards of only that user which is equivalent 
        #to currently logged in user
        stripeCards = StripeModel.objects.filter(user=request.user)
        serializer = CardsListSerializer(stripeCards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# get user details
class UserAccountDetailsView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except:
            return Response({"details": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# update user account
class UserAccountUpdateView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        user = User.objects.get(id=pk)
        data = request.data

        if user:
            if request.user.id == user.id:
                user.username = data["username"]
                user.email = data["email"]

                if data["password"] != "":
                    user.password = make_password(data["password"])

                user.save()
                serializer = UserSerializer(user, many=False)
                message = {"details": "User Successfully Updated.", "user": serializer.data}
                return Response(message, status=status.HTTP_200_OK)
            else:
                return Response({"details": "Permission Denied."}, status.status.HTTP_403_FORBIDDEN)
        else:
            return Response({"details": "User not found."}, status=status.HTTP_404_NOT_FOUND)


# delete user account
class UserAccountDeleteView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):

        try:
            user = User.objects.get(id=pk)
            data = request.data

            if request.user.id == user.id:
                if check_password(data["password"], user.password):
                    user.delete()
                    return Response({"details": "User successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({"details": "Incorrect password."}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"details": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"details": "User not found."}, status=status.HTTP_404_NOT_FOUND)


# get billing address (details of user address, all addresses)
class UserAddressesListView(APIView):

    def get(self, request):
        user = request.user
        user_address = BillingAddress.objects.filter(user=user)
        serializer = BillingAddressSerializer(user_address, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


# get specific address only
class UserAddressDetailsView(APIView):

    def get(self, request, pk):
        user_address = BillingAddress.objects.get(id=pk)
        serializer = BillingAddressSerializer(user_address, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


# create billing address
class CreateUserAddressView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        
        new_address = {
            "name": request.data["name"],
            "user": request.user.id,
            "phone_number": request.data["phone_number"],
            "pin_code": request.data["pin_code"],
            "house_no": request.data["house_no"],
            "landmark": request.data["landmark"],
            "city": request.data["city"],
            "state": request.data["state"],
        }

        serializer = BillingAddressSerializer(data=new_address, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# edit billing address
class UpdateUserAddressView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        data = request.data

        try:
            user_address = BillingAddress.objects.get(id=pk)

            if request.user.id == user_address.user.id:

                updated_address = {
                    "name": data["name"] if data["name"] else user_address.name,
                    "user": request.user.id,
                    "phone_number": data["phone_number"] if data["phone_number"] else user_address.phone_number,
                    "pin_code": data["pin_code"] if data["pin_code"] else user_address.pin_code,
                    "house_no": data["house_no"] if data["house_no"] else user_address.house_no,
                    "landmark": data["landmark"] if data["landmark"] else user_address.landmark,
                    "city": data["city"] if data["city"] else user_address.city,
                    "state": data["state"] if data["state"] else user_address.state,
                }

                serializer = BillingAddressSerializer(user_address, data=updated_address)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"details": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"details": "Not found."}, status=status.HTTP_404_NOT_FOUND)


# delete address
class DeleteUserAddressView(APIView):

    def delete(self, request, pk):
        
        try:
            user_address = BillingAddress.objects.get(id=pk)

            if request.user.id == user_address.user.id:
                user_address.delete()
                return Response({"details": "Address successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"details": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"details": "Not found."}, status=status.HTTP_404_NOT_FOUND)


# all orders list
class OrdersListView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        user_staff_status = request.user.is_staff
        
        if user_staff_status:
            all_users_orders = OrderModel.objects.all()
            serializer = AllOrdersListSerializer(all_users_orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            all_orders = OrderModel.objects.filter(user=request.user)
            serializer = AllOrdersListSerializer(all_orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

# change order delivered status
class ChangeOrderStatus(APIView):

    permission_classes = [permissions.IsAdminUser]

    def put(self, request, pk):
        data = request.data       
        order = OrderModel.objects.get(id=pk)

        # only update this
        order.is_delivered = data["is_delivered"]
        order.delivered_at = data["delivered_at"]
        order.save()
        
        
        serializer = AllOrdersListSerializer(order, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
class UserAPIView(mixins.CreateModelMixin, 
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        # print(request.data)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        # print(serializer.initial_data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=204)
        # print(serializer.errors)
        return Response(status=400)

class UserByUsernameView(APIView):
    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        serializer = UserSerializer(user)
        data = serializer.data
        # Users' Tweets
        tweets = Tweet.objects.filter(user=user).order_by('-created_at')

        # Users' Tweets' Pagination
        tweets_page = self.request.query_params.get('tweets_page', 1)
        tweets_paginator = Paginator(tweets, MAX_PAGE_LENGTH)
        data['tweets_pages'] = tweets_paginator.num_pages
        data['tweets'] = TweetUserSerializer(tweets_paginator.get_page(tweets_page), many=True).data

        # Users' Tweets' Likes Count and liked by user
        if isinstance(data['tweets'], list):
            for tweet in data['tweets']:
                likes_set = TweetLike.objects.filter(tweet=tweet['id'])
                tweet['likes_count'] = likes_set.count()
                likes_set = likes_set.filter(user=request.user)
                tweet['likes'] = TweetLikeSerializer(
                    likes_set,
                    many=True
                ).data

        # Users' Media
        media = tweets.exclude(image__isnull=True).exclude(image='')

        # Users' Media' Pagination
        media_page = self.request.query_params.get('media_page', 1)
        media_paginator = Paginator(media, MAX_PAGE_LENGTH)
        data['media_pages'] = media_paginator.num_pages
        data['media'] = TweetUserSerializer(media_paginator.get_page(media_page), many=True).data

        # Users' Media' Likes Count and liked by user
        if isinstance(data['media'], list):
            for tweet in data['media']:
                likes_set = TweetLike.objects.filter(tweet=tweet['id'])
                tweet['likes_count'] = likes_set.count()
                likes_set = likes_set.filter(user=request.user)
                tweet['likes'] = TweetLikeSerializer(
                    likes_set,
                    many=True
                ).data

        # Users' Likes
        likes = TweetLike.objects.filter(user=user).order_by('-created_at')

        # Users' Likes' Pagination
        likes_page = self.request.query_params.get('likes_page', 1)
        likes_paginator = Paginator(likes, MAX_PAGE_LENGTH)
        data['likes_pages'] = likes_paginator.num_pages
        data['likes'] = TweetLikeExposeTweetSerializer(likes_paginator.get_page(likes_page), many=True).data

        # Users' LikedTweets' Likes Count and liked by user
        if isinstance(data['likes'], list):
            for tweetLike in data['likes']:
                likes_set = TweetLike.objects.filter(tweet=tweetLike['tweet']['id'])
                tweetLike['tweet']['likes_count'] = likes_set.count()
                likes_set = likes_set.filter(user=request.user)
                tweetLike['tweet']['likes'] = TweetLikeSerializer(
                    likes_set,
                    many=True
                ).data
        # Users' Followings
        followings = UserFollower.objects.filter(follower=user).order_by('-created_at')
        data['followings'] = UserFollowerExposeUserSerializer(followings, many=True).data
        data['followings_count'] = followings.count()
        # Users' Followers
        followers = UserFollower.objects.filter(user=user).order_by('-created_at')
        data['followers'] = UserFollowerExposeFollowerSerializer(followers, many=True).data
        data['followers_count'] = followers.count()
        return Response(data)

class TweetAPIView(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    pages = 0

    def get_queryset(self):
        queryset = Tweet.objects.all()
        # show latest tweets first if sort=latest
        sort = self.request.query_params.get('sort', None)
        if sort and sort.lower() == 'latest':
            queryset = queryset.order_by('-created_at')
        # show following tweets if filter=following
        filter = self.request.query_params.get('filter', None)
        if filter and filter.lower() == 'following':
            followings = UserFollower.objects.filter(follower=self.request.user)
            users_following = []
            for following in followings:
                users_following.append(following.user)
            queryset = queryset.filter(user__in=users_following)
        
        # Tweets' Pagination
        page = self.request.query_params.get('page', 1)
        paginator = Paginator(queryset, MAX_PAGE_LENGTH)
        queryset = paginator.get_page(page)
        self.pages = paginator.num_pages
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TweetUserSerializer
        else:
            return TweetWithoutUserSerializer
        
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # show tweet likes if ?related=likes
        related = self.request.query_params.get('related', None)
        if related and (related.lower() == 'likes_all' or related.lower() == 'likes_current'):
            if isinstance(serializer.data, list):
                for tweet in serializer.data:
                    likes_set = TweetLike.objects.filter(tweet=tweet['id'])
                    tweet['likes_count'] = likes_set.count()

                    if related.lower() == 'likes_current': # Only retrieve current user's likes
                        likes_set = likes_set.filter(user=request.user)

                    tweet['likes'] = TweetLikeSerializer(
                        likes_set,
                        many=True
                    ).data

                    # add props to show if user is following the tweet
                    tweet['is_following'] = False
                    followings = UserFollower.objects.filter(follower=request.user)
                    for following in followings:
                        if following.user.id == tweet['user']['id']:
                            tweet['is_following'] = True
                            break

        return Response(serializer.data, headers={'pages': self.pages})
    
    def perform_create(self, serializer):
        kwargs = {
            'user': self.request.user, 
            'text': serializer.validated_data['text'],
            'image': serializer.validated_data['image'],
        }
        serializer.save(**kwargs)

    def perform_update(self, serializer, **kwargs):
        tweet = self.get_object()
        # disable update other user' tweets
        if (tweet.user != self.request.user):
            raise CannotActionOtherUserInfoError(action='update', info='tweets')
        serializer.save(**kwargs)
    
    def perform_destroy(self, instance):
        tweet = self.get_object()
        # disable delete other user' tweets
        if (tweet.user != self.request.user):
            raise CannotActionOtherUserInfoError(action='delete', info='tweets')
        instance.delete()

class TweetLikeAPIView(viewsets.ModelViewSet):
    queryset = TweetLike.objects.all()

    def get_queryset(self):
        queryset = TweetLike.objects.all()

        current_user_query = self.request.query_params.get('current', None)
        tweet_query = self.request.query_params.get('tweet', None)

        valid_current_user_query = current_user_query and current_user_query.lower() == 'true'

        if valid_current_user_query:
            # filter tweet likes for current user
            queryset = queryset.filter(user=self.request.user.id)
        if tweet_query:
            # filter tweet likes for specified tweet
            queryset = queryset.filter(tweet=tweet_query)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TweetLikeSerializer
        else:
            return TweetLikeWithoutUserSerializer

    def perform_create(self, serializer):
        kwargs = {
            'user': self.request.user, 
            'tweet': serializer.validated_data['tweet']
        }
        serializer.save(**kwargs)
    
    def perform_update(self, serializer, **kwargs):
        tweetLike = self.get_object()
        # disable update other user' tweet likes
        if (tweetLike.user != self.request.user):
            raise CannotActionOtherUserInfoError(action='update', info='tweet likes')
        serializer.save(**kwargs)
    
    def perform_destroy(self, instance):
        tweetLike = self.get_object()
        # disable delete other user' tweet likes
        if (tweetLike.user != self.request.user):
            raise CannotActionOtherUserInfoError(action='delete', info='tweet likes')
        instance.delete()
    

class FollowAPIView(viewsets.ModelViewSet):
    queryset = UserFollower.objects.all()

    def get_queryset(self):
        queryset = UserFollower.objects.all()

        current_user_query = self.request.query_params.get('current', None)
        user_query = self.request.query_params.get('user', None)

        valid_current_user_query = current_user_query and current_user_query.lower() == 'true'

        if valid_current_user_query:
            # filter current user's follows
            queryset = queryset.filter(follower=self.request.user.id)
        if user_query:
            # filter follows for specified user
            queryset = queryset.filter(user=user_query)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserFollowerSerializer
        else:
            return UserFollowerWithoutFollowerSerializer

    def perform_create(self, serializer):
        kwargs = {
            'follower': self.request.user, 
            'user': serializer.validated_data['user']
        }
        # Deny follow self
        if kwargs['user'].id == self.request.user.id:
            raise CannotFollowSelfError()
        serializer.save(**kwargs)

    def perform_update(self, serializer, **kwargs):
        follow = self.get_object()
        # disable update other user' follows
        if (follow.follower != self.request.user):
            raise CannotActionOtherUserInfoError(action='update', info='follows')
        # Deny follow self
        if serializer.validated_data['user'].id == self.request.user.id:
            raise CannotFollowSelfError()
        serializer.save(**kwargs)
    
    def perform_destroy(self, instance):
        follow = self.get_object()
        # disable delete other user' follows
        if (follow.follower != self.request.user):
            raise CannotActionOtherUserInfoError(action='delete', info='follows')
        instance.delete()



