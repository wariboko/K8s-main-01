from django.contrib.auth.models import AbstractUser
from django.db import models

from PIL import Image
from PIL.Image import core as _imaging
from django.conf import settings
from django.conf.urls.static import static


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=25)


    def __str__(self):
        return f"{self.category}"

class Auction(models.Model):
    id = models.AutoField(primary_key=True)

    STATUS = (
        ('Active', 'Active'),
        ('Closed', 'Closed'),
        ('Sold', 'Sold'),
    )
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    active = models.CharField(max_length=25, choices=STATUS)
    selectcategory = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media", blank=True)
    date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.seller}, {self.title}, {self.description}, {self.active}, {self.price}, {self.date},{self.active}, {self.image}"


class PostImage(models.Model):
    id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, default=None, on_delete=models.CASCADE, related_name="postImage")
    images = models.ImageField(upload_to="media/", blank=True)

    def __str__(self):
        return self.auction.title


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer_name")
    product_id = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="product_bids")
    product_price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer}, {self.product_price}, {self.date}"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="product_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return f"{self.user},  {self.comment}, {self.product_id}"

class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
    product_id = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="product_watchlist")

    def __str__(self):
        return f"{self.user}, {self.product_id}"
