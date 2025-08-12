from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from .serializers import UserRegisterSerializer, ProductSerializer
from rest_framework.views import APIView

from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from django.http import HttpResponse

from django.contrib.auth.models import User
from .models import Wishlist, Product, SearchLogs
from django.db.models import Subquery
from django.db.models import Q

from django.forms.models import model_to_dict
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

@api_view(["POST",])
def logout_user(request):
    if request.method == "POST":

        if request.user.is_anonymous:
            return Response({"Message": "Anonymous User"}, status=status.HTTP_403_FORBIDDEN)
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            logout(request)
            request.session.flush()
        except Token.DoesNotExist:
            pass

        
        return Response({"Message": "You are logged out"}, status=status.HTTP_200_OK)

@api_view(["POST",])
@permission_classes([AllowAny]) #making route public
def user_register_view(request):
    if request.method == "POST":
        try:
            serializer = UserRegisterSerializer(data=request.data)
        except:
            return Response({'error' : 'username, password, password2, email are required in valid format' })
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            
            data['response'] = 'Account has been created'
            data['username'] = account.username
            data['email'] = account.email
            
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)
    

def home(request):
    return HttpResponse("Welcome to the Home Page!")


@api_view(['GET'])
def profile(request):
    if request.user.is_authenticated:
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
        })
    else:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


# @api_view(['GET'])
# def search(request):
#     query = request.GET.get('q', '') 
#     return Response({"search_query": query, "results": []})


#updated search view 
@api_view(['GET'])
def search(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return Response({"error": "No search query provided."}, status=status.HTTP_400_BAD_REQUEST)

    # Filter products
    products = Product.objects.filter(
        status="active"
    ).filter(
        Q(name__icontains=query) | Q(brand__icontains=query)
        # models.Q(name__icontains=query) | models.Q(brand__icontains=query)
    )

    # Save search logs if user is authenticated
    if request.user.is_authenticated:
        SearchLogs.objects.create(
            query_string=query,
            username=request.user
        )

    data = [model_to_dict(product) for product in products]
    return Response({"search_query": query, "results": data}, status=status.HTTP_200_OK)

class ProductView(APIView):

    permission_classes = []

    def get(self, request):

        products = Product.objects.filter(status='active').all()
        data = [model_to_dict(product) for product in products]
        return Response(data, status=status.HTTP_200_OK)


class WishlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wishlist_product_ids = Wishlist.objects.filter(
            username=request.user, status=True
        ).values_list('product_id', flat=True)

        products = Product.objects.filter(id__in=wishlist_product_ids).values('id', 'name', 'price')
        return Response(list(products), status=status.HTTP_200_OK)

    def post(self, request):
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        Wishlist.objects.create(username=request.user, product_id=product_id, status=True)
        return Response({"message": "Product added to wishlist."}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        wishlist_item = Wishlist.objects.filter(username=request.user, product_id=product_id, status=True)
        if not wishlist_item.exists():
            return Response({"error": "Product not found in wishlist."}, status=status.HTTP_404_NOT_FOUND)

        wishlist_item.update(status=False)
        return Response({"message": "Product removed from wishlist."}, status=status.HTTP_200_OK)


# login endpoimt

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key})
