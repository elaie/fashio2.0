from django.urls import path, include
from account import views
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import routers


api_router = routers.DefaultRouter()
api_router.register(r'user', views.UserAPIView)
api_router.register(r'tweet', views.TweetAPIView)
api_router.register(r'tweet_like', views.TweetLikeAPIView)
api_router.register(r'follow', views.FollowAPIView)
print("API ROUTER"+str(api_router))
urlpatterns = [

    # user
    path('register/', views.UserRegisterView.as_view(), name="register-page"),
    path('login/', views.MyTokenObtainPairView.as_view(), name="login-page"),
    path('user/<int:pk>/', views.UserAccountDetailsView.as_view(), name="user-details"),
    path('user_update/<int:pk>/', views.UserAccountUpdateView.as_view(), name="user-update"),
    path('user_delete/<int:pk>/', views.UserAccountDeleteView.as_view(), name="user-delete"),

    # user address
    path('all-address-details/', views.UserAddressesListView.as_view(), name="all-address-details"),
    path('address-details/<int:pk>/', views.UserAddressDetailsView.as_view(), name="address-details"),
    path('create-address/', views.CreateUserAddressView.as_view(), name="create-address"),
    path('update-address/<int:pk>/', views.UpdateUserAddressView.as_view(), name="update-address-details"),
    path('delete-address/<int:pk>/', views.DeleteUserAddressView.as_view(), name="delete-address"),

    # order
    path('all-orders-list/', views.OrdersListView.as_view(), name="all-orders-list"),
    path('change-order-status/<int:pk>/', views.ChangeOrderStatus.as_view(), name="change-order-status"),

    # stripe
    path('stripe-cards/', views.CardsListView.as_view(), name="stripe-cards-list-page"),

    
     # --------------------- API
    path('api/', include(api_router.urls)),
    path('api/current_user/', views.CurrentUserView.as_view(), name="current_user"),
    path('api/username/<str:username>/', views.UserByUsernameView.as_view(), name="current_user"),
]
print("PATH: "+str(urlpatterns[13]))