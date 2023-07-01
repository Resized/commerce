from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import IntegrityError
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, AuctionListing, Bid


def index(request):
    return render(request, "auctions/index.html", {
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
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "user": request.user
    })


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

    if request.method == "POST":
        form = CreateBidForm(request.POST, initial={"current_price": listing.current_price})
        if request.user == listing.user:
            form.add_error('amount', "Cannot bid on yor own listing.")
        if request.user == listing.current_price:
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
        "user": request.user
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
            print("hello")
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
                current_price=current_price
            )

            listing.save()

            return HttpResponseRedirect(reverse("index"))
    else:
        form = CreateListingForm()
    return render(request, "auctions/create_listing.html", {"form": form})


@login_required(login_url="login")
def watchlist(request):
    return None
