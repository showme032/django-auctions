from django.contrib import admin
from .models import *

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "auctioneer", "category", "price", "active")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "listing")

class BidAdmin(admin.ModelAdmin):
    list_display = ("listing",  "bidder", "price")


# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)