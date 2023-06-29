from django.contrib import admin

from .models import Comment, User, AuctionListing, Bid, Category

# Register your models here.

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(AuctionListing)
admin.site.register(Bid)
admin.site.register(Category)
