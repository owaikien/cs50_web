from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from decimal import Decimal


from .models import User, Listing, Category, Comment, Bid


def index(request):
    activeListing = Listing.objects.filter(isActive=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": activeListing,
        "categories": allCategories
    })

def chooseCategory(request):
    if request.method == 'POST':
        category_from_input = request.POST['category']
        category = Category.objects.get(categoryName = category_from_input)
        activeListing = Listing.objects.filter(isActive=True, category=category)
        allCategories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": activeListing,
            "categories": allCategories,
        })
    
def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    isListingInWatchList = request.user in listingData.watchList.all()
    allComments = Comment.objects.filter(listing=listingData)

    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListing": isListingInWatchList,
        "allComments": allComments
    })

def removeWatchList(request, id):
    listingData = Listing.objects.get(pk=id)
    user = request.user
    listingData.watchList.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))
    
def addWatchList(request, id):
    listingData = Listing.objects.get(pk=id)
    user = request.user
    listingData.watchList.add(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def WatchList(request):
    user = request.user
    listings = user.listingWatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def addComments(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['newComment']

    newComment = Comment(
        owner=currentUser,
        listing = listingData,
        comments=message
    )

    newComment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def bid(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user

    if request.method == "POST":
        bid_amount = Decimal(request.POST['bid'])
        if bid_amount < listing.price.bid or (request.user != listing.price.owner and bid_amount <= listing.price.bid):
            messages.error(request, "Your bid must be higher than the current price/bid!")
        else:
            new_bid = Bid.objects.create(bid=bid_amount, owner=user)
            listing.price = new_bid
            listing.save()

    return HttpResponseRedirect(reverse("listing", args=(id, ))) 

def close(request, id):
    listing = Listing.objects.get(pk=id)
    user=request.user

    if user == listing.owner:
        listing.isActive = False
        listing.save()

    return HttpResponseRedirect(reverse("listing", args=(id,)))


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
    
def create(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": allCategories
        })

    else:
        # get the new objects from `create.html` form
        title = request.POST['title']
        description = request.POST['description']
        imageurl = request.POST['imageurl']
        
        # bid price
        price = float(request.POST['price'])
        bid = Bid.objects.create(bid=price, owner=request.user)

        category = request.POST['category']

        # Get the user
        user = request.user
        
        # get the category from all categories    
        categoryData = Category.objects.get(categoryName=category)
        
        # Create a new Listing using the new objects defined 
        NewListing = Listing(
            title= title,
            description= description,
            price= bid,
            imageurl= imageurl,
            category= categoryData,
            owner=user
        )

        # Insert the objects into our database
        NewListing.save()

        # Redirect into new page 
        return HttpResponseRedirect(reverse(index))