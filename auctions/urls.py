from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.all_categories, name="all_categories"),
    path("categories/<int:category_id>", views.view_category, name="view_category"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listings/<int:listing_id>", views.view_listing, name="view_listing"),
    path("listings/<int:listing_id>/bid", views.bid, name="bid"),
    path("listings/<int:listing_id>/close", views.close_listing, name="close_listing"),
    path("watchlist", views.view_watchlist, name="view_watchlist"),
    path("listings/<int:listing_id>/watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("listings/<int:listing_id>/comment", views.add_comment, name="add_comment"),
]
