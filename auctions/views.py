from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.validators import MinValueValidator
from django.db import IntegrityError
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, AuctionListing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "title": "Active Listings",
        "listings": AuctionListing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def view_listing(request, listing_id):
    try:
        listing = AuctionListing.objects.get(pk=listing_id)
    except AuctionListing.DoesNotExist:
        return HttpResponse("Invalid listing")
    is_watched = get_is_watched(request, listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "user": request.user,
        "is_watched": is_watched
    })


def get_is_watched(request, listing_id):
    is_watched = False
    if request.user.is_authenticated:
        watchlist = User.objects.get(pk=request.user.id).watchlist
        if watchlist.filter(pk=listing_id).exists():
            is_watched = True
    return is_watched


class CreateBidForm(forms.Form):
    amount = forms.DecimalField(
        min_value=0,
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount and amount <= self.initial["current_price"]:
            raise forms.ValidationError("Bid amount must be greater than the current price.")
        return amount


@login_required(login_url="login")
def bid(request, listing_id):
    try:
        listing = AuctionListing.objects.get(pk=listing_id)
    except AuctionListing.DoesNotExist:
        return HttpResponse("Invalid listing")
    is_watched = get_is_watched(request, listing_id)
    if request.method == "POST":
        form = CreateBidForm(request.POST, initial={"current_price": listing.current_price})
        if request.user == listing.user:
            form.add_error('amount', "Cannot bid on yor own listing.")
        if listing.bids.all() and request.user == listing.bids.last().user:
            form.add_error('amount', "You already have the highest bid.")

        if form.is_valid():
            amount = form.cleaned_data["amount"]

            new_bid = Bid(
                user=request.user,
                listing=listing,
                amount=amount
            )
            new_bid.save()

            listing.current_price = amount
            listing.save()

            return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))
    else:
        form = CreateBidForm(initial={"current_price": listing.current_price})

    return render(request, "auctions/listing.html", {
        "form": form,
        "listing": listing,
        "user": request.user,
        "is_watched": is_watched
    })


class CreateListingForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField()
    current_price = forms.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    category = forms.ModelChoiceField(empty_label="Select a category (optional)", queryset=Category.objects.all(),
                                      required=False)
    image_url = forms.URLField(required=False)


@login_required(login_url="login")
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            current_price = form.cleaned_data["current_price"]
            category = form.cleaned_data["category"]
            image_url = form.cleaned_data["image_url"]

            listing = AuctionListing(
                title=title,
                description=description,
                category=category,
                user=request.user,
                image_url=image_url,
                current_price=current_price,
                is_active=True
            )

            listing.save()

            return HttpResponseRedirect(reverse("index"))
    else:
        form = CreateListingForm()
    return render(request, "auctions/create_listing.html", {"form": form})


@login_required(login_url="login")
def add_to_watchlist(request, listing_id):
    watchlist = User.objects.get(pk=request.user.id).watchlist
    if watchlist.filter(pk=listing_id).exists():
        watchlist.remove(listing_id)
    else:
        watchlist.add(listing_id)
    return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))


def view_watchlist(request):
    return render(request, "auctions/index.html", {
        "title": "My Watchlist",
        "listings": User.objects.get(pk=request.user.id).watchlist.all()
    })


@login_required(login_url="login")
def close_listing(request, listing_id):
    try:
        listing = AuctionListing.objects.get(pk=listing_id)
    except AuctionListing.DoesNotExist:
        return HttpResponse("Invalid listing")

    if request.user == listing.user:
        listing.is_active = False
        listing.save()

    return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))


class CreateCommentForm(forms.Form):
    comment = forms.CharField(max_length=255)


@login_required(login_url="login")
def add_comment(request, listing_id):
    try:
        listing = AuctionListing.objects.get(pk=listing_id)
    except AuctionListing.DoesNotExist:
        return HttpResponse("Invalid listing")

    if request.method == "POST":
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            new_comment = Comment(
                listing=listing,
                user=request.user,
                content=comment
            )

            new_comment.save()

            return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))

    else:
        print("hello world")
        form = CreateCommentForm()

    return render(request, "auctions/listing.html", {
        "form": form,
        "listing": listing,
        "user": request.user
    })


def all_categories(request):
    return render(request, "auctions/categories.html", {
        "title": "All Categories",
        "categories": Category.objects.all()
    })


def view_category(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return HttpResponse("Invalid listing")

    return render(request, "auctions/index.html", {
        "title": category.name,
        "listings": category.listings.all()
    })
