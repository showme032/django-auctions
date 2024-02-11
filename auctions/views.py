from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Category, User, Listing, Comment, Bid    


#render index page with all the listings
def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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


#let the logged-in user create new listing
@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        image = request.POST["image"]
        category = request.POST["category"]
        description = request.POST["description"]
        price = request.POST["price"]

        #create listing with provided info
        new_listing = Listing(
            auctioneer = request.user,
            title = title,
            image = image,
            category = Category.objects.get(name=category),
            description = description,
            price = price
        )
        new_listing.save()

        #create the bidding data for the created listing
        bid = Bid.objects.create(listing=new_listing, price=price, bidder=request.user)
        bid.save()

        return HttpResponseRedirect(reverse("index"))
            
    return render(request, "auctions/create.html", {
        "categories": Category.objects.all()
    })


#view listing page
def view_listing(request, listing_id, *message):
    listing = Listing.objects.get(pk=listing_id)
    listing_bid = Bid.objects.get(listing=listing)
    comments = Comment.objects.filter(listing=listing)

    return render(request, "auctions/listing.html",{
        "listing": listing,
        "listing_bid": listing_bid,
        "comments": comments
    })


#add listing to users watchlist
def watch(request, listing_id):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = Listing.objects.get(pk=listing_id)

        #if the listing isn't already added, add to watchlist
        if request.POST["added"] == "False":
            request.user.watchlist.add(listing)
        if request.POST["added"] == "True":
            request.user.watchlist.remove(listing)
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


#view the list of watched listing
def watchlist(request):
    watched_items = request.user.watchlist.all()

    return render(request, "auctions/watchlist.html",{
        "watched_items": watched_items
    })


#place the users bid on listing
def bid(request, listing_id):
    if request.method == "POST":
        #get listing, user-placed bid and listings current bid
        listing_id = request.POST["listing_id"]
        user_bid = int(request.POST["user_bid"])
        listing = Listing.objects.get(pk=listing_id)
        listing_bid = Bid.objects.get(listing=listing)
        
        #if placed bid is bigger than the current one, update the data
        if user_bid > listing.price:
            listing_bid.price = user_bid
            listing_bid.bidder = request.user
            listing_bid.save()

            listing.price = user_bid          
            listing.save()

        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


#close the auction
def close(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        listing.active = False
        listing.save()

        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


#add the comment to the listing
def add_comment(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        comment_text = request.POST["comment_text"]
        user = request.user

        comment = Comment(listing=listing, user=user, comment_text=comment_text)
        comment.save()

        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


#view listing categories
def categories(request):
    category_list = Category.objects.all()
    listings = Listing.objects.all()

    return render(request, "auctions/categories.html", {
        "category_list": category_list,
        "listings": listings
    })