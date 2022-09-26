from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category_view, name="category"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("manage_watchlist/<int:listing_id>", views.manage_watchlist, name="manage_watchlist"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("bid/<int:listing_id>", views.make_bid, name="bid"),
    path("close/<int:listing_id>", views.close, name="close")
]
