from django.contrib import admin
from shop.models import Product, Wishlist, SearchLogs
# Register your models here.


admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(SearchLogs)