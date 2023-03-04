from .models import Product
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.decorators import permission_classes
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
class ProductView(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):

    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductCreateView(APIView):

    def post(self, request):
        user = request.user
        data = request.data

        product = {
            "product_from": data["product_from"],
            "name": data["name"],
            "description": data["description"],
            "price": data["price"],
            "stock": data["stock"],
            "image": data["image"],
            "image2": data["image2"],
            "image3": data["image3"],
        }

        serializer = ProductSerializer(data=product, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProductEditView(APIView):
    
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, pk):
        data = request.data
        product = Product.objects.get(id=pk)
        
        updated_product = {
            "product_from": data["product_from"] if data["product_from"] else product.product_from,
            "name": data["name"] if data["name"] else product.name,
            "description": data["description"] if data["description"] else product.description,
            "price": data["price"] if data["price"] else product.price,
            "stock": data["stock"],
            "image": data["image"] if data["image"] else product.image,
            "image2": data["image2"] if data["image2"] else product.image2,
            "image3": data["image3"] if data["image3"] else product.image3,
        }

        serializer = ProductSerializer(product, data=updated_product)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class ProductDeleteView(APIView):

    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            product.delete()
            return Response({"detail": "Product successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)



@csrf_exempt
def your_endpoint(request):
    print("YOUR ENDPOINT INIT")
    global USERNAME
    USERNAME = "teststing"
    # if request.method == 'POST':
    #     data = request.POST.get('data')
    #     print("PRINTING DATA")
    #     print(request.POST)
    #     print(data)
    #     return JsonResponse({'message': 'Data received'})
    if request.method == 'POST':
        data = json.loads(request.body)
        variableString = data.get('data')
        print(variableString)  # Check that variableString is not None
        USERNAME = variableString
        print("USERNAME: "+USERNAME)
        return JsonResponse({'message': 'Data received'})

class PostViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_user(request):
        current_user = request.user
        print (current_user.id)

    @action(detail=True, methods=['patch'])
    def like(self, request, pk):
        print("PK ID: ")
        print(pk)
        print("USERNAME INSDE POST VIEW SET: "+USERNAME)
        post = get_object_or_404(Product, pk=pk)
        post.likes += 1
        
        my_list = post.get_my_list()  # get the current list value
        my_list.append(USERNAME)  # add a new item to the list
        post.set_my_list(my_list)
        
        post.save()
        serializer = ProductSerializer(post)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def unlike(self, request, pk=None):
        post = get_object_or_404(Product, pk=pk)
        post.likes -= 1
        
      
        my_list = post.get_my_list()  # get the current list value
        my_list.remove(USERNAME)  # remove the item from the list
        post.set_my_list(my_list)  

        post.save()
        serializer = ProductSerializer(post)
        return Response(serializer.data)

class UserListView(ListView):
    model = Product
    template_name = 'user_list.html'