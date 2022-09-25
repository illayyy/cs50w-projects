from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


def index(request):
    return render(request, "auctions/index.html", {
        "title": "Active Listings",
        "listings": Listing.objects.filter(active=True)
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


def listing_view(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.user in listing.watched_by.all():
        watchlist_text = "Remove from watchlist"
    else:
        watchlist_text = "Add to watchlist"

    current_bid = listing.listing_bids.last()
    if current_bid is None:
        current_bid = listing.starting_bid

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": listing.listing_comments.all(),
        "watchlist_text": watchlist_text,
        "current_bid": current_bid,
        "num_of_bids": len(listing.listing_bids.all()),
    })


def new(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            title = request.POST.get('title')
            desc = request.POST.get('desc')
            price = request.POST.get('price')
            category_id = request.POST.get('category')
            image = request.POST.get('image')

            if title and desc and price:
                if not image:
                    image="https://static.vecteezy.com/system/resources/previews/004/141/669/original/no-photo-or-blank-image-icon-loading-images-or-missing-image-mark-image-not-available-or-image-coming-soon-sign-simple-nature-silhouette-in-frame-isolated-illustration-vector.jpg"

                if not category_id:
                    category = None
                else:
                    category = Category.objects.get(pk=category_id)

                listing = Listing.objects.create(
                    title=title,
                    description=desc,
                    starting_bid=price,
                    category=category,
                    image=image,
                    creator=request.user
                )
                listing.save()
                return redirect('listing', listing.id)
            return render(request, "auctions/new.html", {
                "categories": Category.objects.all(),
                "message": "blank-fields"
            })
        return render(request, "auctions/new.html", {
            "categories": Category.objects.all()
        })
    return redirect('login')


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def category_view(request, category_id):
    category = Category.objects.get(pk=category_id)
    category_listings = category.category_listings.filter(active=True)
    return render(request, "auctions/index.html", {
        "title": category,
        "listings": category_listings
    })


def comment(request, listing_id):
    content = request.POST.get('content')
    if content:
        c = Comment.objects.create(
            creator=request.user,
            listing=Listing.objects.get(pk=listing_id),
            content=content
        )
        c.save()
    return redirect('listing', listing_id)


def manage_watchlist(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    if user in listing.watched_by.all():
        listing.watched_by.remove(user)
    else:
        listing.watched_by.add(user)
    return redirect('listing', listing_id)


def watchlist_view(request):
    if request.user.is_authenticated:
        return render(request, "auctions/index.html", {
            "title": f"{request.user}'s Watchlist",
            "listings": request.user.user_watchlist.all()
        })
    return redirect('login')


def make_bid(request, listing_id):
    bid_val = float(request.POST.get('bid'))
    listing = Listing.objects.get(pk=listing_id)
    current_bid = listing.listing_bids.last()

    if current_bid is None:
        current_bid_val = listing.starting_bid
    else:
        current_bid_val = current_bid.value

    if bid_val > current_bid_val:
        bid = Bid.objects.create(
            value=bid_val,
            creator=request.user,
            listing=listing
        )
        bid.save()
        message = "success"
        current_bid_val = bid_val
    else:
        message = "too-low"

    if request.user in listing.watched_by.all():
        watchlist_text = "Remove from watchlist"
    else:
        watchlist_text = "Add to watchlist"

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": listing.listing_comments.all(),
        "watchlist_text": watchlist_text,
        "current_bid": current_bid_val,
        "num_of_bids": len(listing.listing_bids.all()),
        "message": message
    })


def close(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.active = False
    listing.save()
    return redirect('listing', listing_id)
