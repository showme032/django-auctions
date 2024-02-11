from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="watchers")


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Listing(models.Model):
    auctioneer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    image = models.URLField(max_length=200, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="items")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment",)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    comment_text = models.TextField()

    def __str__(self):
        return f"{self.user}: {self.comment_text}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids",)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bidder  = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="bids")

    def save(self, *args, **kwargs):
        if self.price > self.listing.price:
            self.listing.price = self.price
            self.listing.save()
        super().save(*args, **kwargs)
    
    