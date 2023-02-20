from django.urls import path
from posts import views


urlpatterns = [
    path('post/', views.PostView.as_view(), name="products-list"),
    path('post/<str:pk>/', views.PostDetailView.as_view(), name="post-details"),
    path('post-create/',views.PostCreateView.as_view(),name='post-create'),
    path('post-update/<str:pk>/', views.PostEditView.as_view(), name="post-update"),
    path('post-delete/<str:pk>/', views.PostDeleteView.as_view(), name="post-delete"),

    ]