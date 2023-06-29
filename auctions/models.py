from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class AuctionListing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    watchlisted_by = models.ManyToManyField(User, related_name="watchlist")

    def __str__(self):
        return f"{self.id} - {self.title}"


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()


class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
