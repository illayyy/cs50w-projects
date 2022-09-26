from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_listings")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="category_listings", blank=True,
                                 null=True)
    description = models.CharField(max_length=1024)
    image = models.CharField(max_length=256)
    watched_by = models.ManyToManyField(User, related_name="user_watchlist", blank=True)
    starting_bid = models.FloatField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} by {self.creator} in category: {self.category}"


class Comment(models.Model):
    content = models.CharField(max_length=2048)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")

    def __str__(self):
        return f"{self.creator}: '{self.content}' on {self.listing.title} by {self.listing.creator}"


class Bid(models.Model):
    value = models.FloatField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")

    def __str__(self):
        return f"{self.creator}: {self.value}$ for {self.listing.title} by {self.listing.creator}"
