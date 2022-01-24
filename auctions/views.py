from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import *
from django.core.files.storage import FileSystemStorage
import os, os.path
from django.contrib import messages

def index(request):
    #Get all objects in both models and render them.
   
    return render(request, "auctions/index.html",{
        "auctions": Auction.objects.all(),
        "photos": PostImage.objects.all(),
        "categories": Category.objects.all()
    })

def indexItem(request, auction_id):
    product = Auction.objects.get(pk = auction_id)
    postImage = PostImage.objects.filter(auction=auction_id)
    return render(request, "auctions/index_view.html",{
        'product': product,
        'postImage': postImage,
        "categories": Category.objects.all()
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
            #logging.info(f'{username} logged in.')
            return HttpResponseRedirect(reverse("index"))
        else:
            #logging.warning(f'{username} logged in Invalid username and/or password..')
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

            #logging.warning(f'{username}-{email}typed in an incorrect password!')
            
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            #logging.info(f'{username}-{email} just signed up!')
        except IntegrityError:
            #logging.warning(f'{username} already taken')
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def createListing(request):
    if request.method == "POST":
        product = Auction()
        photos = PostImage()
        category = Category.objects.get(id=int(request.POST["category"]))
        
        product.title = request.POST["title"]
        product.seller = request.user
        product.description= request.POST["description"]
        product.active = request.POST["active"]
        product.price = request.POST["price"]
        product.image = request.FILES['image']
        product.selectcategory = category
        product.save()

        # Return the last updated id from product and update it to the PostImage model.
        photos.auction = Auction.objects.latest('id')

        #Get all the images uploaded to the path.
        images = request.FILES.getlist('images')
        
        #Loop through all the images uploaded and post each.
        if images:
            for image in images:
                photos = PostImage.objects.create(images=image, auction=photos.auction)
        photos.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html",{
            "auctions":Auction.objects.all(),
            "categories": Category.objects.all(),
            "photos": PostImage.objects.all()
        })


def categoryList(request,category_id):
    products = Auction.objects.filter(selectcategory=category_id)
    if len(products) >= 1:
        return render(request, "auctions/category.html",{
        "auctions":Auction.objects.all(),
        "products": products,
        "categories": Category.objects.all()
    })

    else: 
        return redirect("index")

def watchlist(request):
    product_watchlist = Watchlist.objects.all().select_related('product_id')
    if product_watchlist:
        return render(request, "auctions/watchlist.html", {
            'product_watchlist': product_watchlist,
            "categories": Category.objects.all()
        })
    else:
        return render(request, "auctions/watchlist.html", {
            "message": "Empty",
            "categories": Category.objects.all()
        })

def addWatchlist(request, auction_id):
    query = Auction.objects.get(pk = auction_id)
    Watchlist.objects.create(user = request.user, product_id = query)
    return redirect(watchlist)
   
def remove_watchlist(request, auction_id):
    query = Watchlist.objects.filter(user = request.user, product_id = auction_id)
    print(query)
    if query:

        query.delete()

    return HttpResponseRedirect(reverse("watchlist"))



          


        
