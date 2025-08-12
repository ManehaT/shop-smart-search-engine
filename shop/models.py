from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.utils import timezone
from urllib.parse import unquote_plus
from django.contrib.auth.models import User
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def decode_keyword(encoded_str):
    return unquote_plus(encoded_str)

class Product(models.Model):

    name = models.CharField(max_length=255)
    image_url = models.CharField(max_length=500)
    product_url = models.CharField(max_length=500)
    category = models.CharField(max_length=100, default=None)
    brand = models.CharField(max_length=100, default=None)
    price = models.IntegerField()
    sale_price = models.IntegerField()
    status = models.CharField(max_length=10, default="active")
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=50)

class Wishlist(models.Model):
    product_id = models.IntegerField()
    username = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

class SearchLogs(models.Model):
    query_string = models.CharField(max_length=500)
    keyword = models.CharField(max_length=255)
    username = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    
    # def save(self):
    #     self.keyword = decode_keyword(self.query_string)
    #     super().save()

    #updated save because it wants args
    def save(self, *args, **kwargs):
            self.keyword = decode_keyword(self.query_string)
            super().save(*args, **kwargs)
        