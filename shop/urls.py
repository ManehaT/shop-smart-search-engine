from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [

    # Authentication
    # 
    # path("login/", obtain_auth_token, name="login"),
    path("login/", views.CustomAuthToken.as_view(), name="login"),   # <- use your CustomAuthToken
    path("logout/", views.logout_user, name="logout_user"),
    path("register/", views.user_register_view, name="register"),

    # GET - Get all products
    path("products/", views.ProductView.as_view(), name ="products"),


    # Wishlist URL
    # POST - Add to Wishlist
    # GET - Products in wishlist
    path("wishlist", views.WishlistView.as_view(), name ="wishlist"),

    
]