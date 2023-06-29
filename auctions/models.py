from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=255)


class AuctionListing(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")


class Bid(models.Model):
    pass


class Comment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
