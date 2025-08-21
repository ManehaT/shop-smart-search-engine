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


@api_view(['GET'])
def search(request):
    # get the search term from FE
    query = request.GET.get('q', '').strip()

    #get last 5 search keyword
    if request.user.is_authenticated:
        recent_logs = SearchLogs.objects.filter(
            username=request.user,
            status=True
        ).order_by('-created_at')[:5]
        recent_keywords = [log.keyword for log in recent_logs]
    else:
        recent_keywords = []

    # If a search query is provided, use it
    if query:
        products = Product.objects.filter(
            status="active"
        ).filter(
            Q(name__icontains=query) | Q(brand__icontains=query)
        )

        # Save search logs
        if request.user.is_authenticated:
            SearchLogs.objects.create(
                query_string=query,
                username=request.user
            )

    # If no query, show products based on recent searches
    else:
        if recent_keywords:
            products = Product.objects.filter(status="active").filter(
                Q(name__icontains=recent_keywords[0]) | Q(brand__icontains=recent_keywords[0])
            )
            for kw in recent_keywords[1:]:
                products = products | Product.objects.filter(
                    status="active"
                ).filter(
                    Q(name__icontains=kw) | Q(brand__icontains=kw)
                )
            products = products.distinct()
        else:
            # fallback: show all active products
            products = Product.objects.filter(status="active")

    serializer = ProductSerializer(products, many=True)
    return Response({"search_query": query, "results": serializer.data}, status=status.HTTP_200_OK)


    # if not query:
    #     return Response({"error": "No search query provided."}, status=status.HTTP_400_BAD_REQUEST)

    # # Filter active products in the products table
    # products = Product.objects.filter(
    #     status="active"
    # ).filter(
    #     Q(name__icontains=query) | Q(brand__icontains=query)
    # )
    
    # #converts into json friendly format
    # serializer = ProductSerializer(products, many = True)
    # # Save search logs if user is authenticated
    # if request.user.is_authenticated:
    #     SearchLogs.objects.create(
    #         query_string=query,
    #         username=request.user
    #     )


    # return Response({"search_query": query, "results": serializer.data}, status=status.HTTP_200_OK)
    
# class ProductView(APIView):

#     permission_classes = []

#     def get(self, request):

#         products = Product.objects.filter(status='active').all()
#         data = [model_to_dict(product) for product in products]
#         return Response(data, status=status.HTTP_200_OK)
class ProductView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user  # Get the User object, not just username
        print("User is: ", user.username)

        # Default products
        products_qs = Product.objects.filter(status='active')

        if user.is_authenticated:
            # Get latest search logs for this user - filter by User object
            last_log = SearchLogs.objects.filter(username=user).order_by('-created_at').first()

            if last_log:
                # Example: filter products where name/category/brand contains keyword
                keyword = last_log.keyword
                products_qs = products_qs.filter(
                    Q(name__icontains=keyword) |
                    Q(category__icontains=keyword) |
                    Q(brand__icontains=keyword)
                )

        # Convert queryset to list of dicts
        data = [model_to_dict(product) for product in products_qs]
        return Response(data, status=status.HTTP_200_OK)


class WishlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wishlist_product_ids = Wishlist.objects.filter(
            username=request.user, status=True
        ).values_list('product_id', flat=True)

        print(request.user.username)


        products = Product.objects.filter(id__in=wishlist_product_ids).values('id', 'name', 'price','sale_price','image_url')
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
