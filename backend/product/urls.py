from django.urls import path, include
from product import views
from rest_framework import routers
from .views import PostViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('products/', views.ProductView.as_view(), name="products-list"),
    path('product/<str:pk>/', views.ProductDetailView.as_view(), name="product-details"),
    path('product-create/', views.ProductCreateView.as_view(), name="product-create"),
    path('product-update/<str:pk>/', views.ProductEditView.as_view(), name="product-update"),
    path('product-delete/<str:pk>/', views.ProductDeleteView.as_view(), name="product-delete"),
    path('', include(router.urls)),
    path('your-endpoint/', views.your_endpoint), 
]