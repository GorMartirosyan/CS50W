from django.shortcuts import render
from .models import User, AuctionItem, Comment, Bid
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from .forms import AuctionItemForm, CommentForm
# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ValidationError

def home(requst):
    return render(requst, 'auctions/home.html', {
        "auctionItems": AuctionItem.objects.all()
    })

def signin(request):
    if request.method == "GET":
        return render(request, 'auctions/signin.html')
    else:
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "auctions/signin.html", {
                "message": "Invalid username and/or password."
            })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))

def register(request):
    if request.method == "GET":
        return render(request, 'auctions/register.html')
    else:
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
        return HttpResponseRedirect(reverse("home"))
    
def create(request):
    if request.method == "GET":
        return render(request, 'auctions/create.html', {
            "form": AuctionItemForm()
        })
    else:
        form = AuctionItemForm(request.POST)
        if form.is_valid():
            auction_item = AuctionItem(owner=request.user, **form.cleaned_data)
            if not auction_item.image_url:
                auction_item.image_url = 'https://user-images.githubusercontent.com/52632898/161646398-6d49eca9-267f-4eab-a5a7-6ba6069d21df.png'
            auction_item.save()    
            starting_bid = auction_item.starting_bid
            bid = Bid(amount=starting_bid, user=request.user, auction=auction_item)
            bid.save()

            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, 'auctions/create.html', {
            'form': form,
            'error': form.errors
        })

def watchlist(request):
    return render(request, 'auctions/watchlist.html', {
        "watchlist": request.user.watchlist.all()
    })

def add_to_watchlist(request, id):
    item = AuctionItem.objects.get(id=id)
    request.user.watchlist.add(item)
    request.user.watchlist_count += 1
    request.user.save()
    return HttpResponseRedirect(reverse('home'))

def remove_from_watchlist(request, id):
    item = AuctionItem.objects.get(id=id)
    request.user.watchlist.remove(item)
    request.user.watchlist_count -= 1
    request.user.save()
    return HttpResponseRedirect(reverse('home'))

def categories(request):
    categories = AuctionItem.objects.values_list('category', flat=True).distinct()
    return render(request, 'auctions/categories.html', {
        "categories" : categories
    })

def category(request, category):
    items = AuctionItem.objects.filter(category=category)
    return render(request, 'auctions/category.html', {
        "auctionItems": items,
        "category" : category
    })

def item(request, id):
    form = CommentForm(request.user)
    item = AuctionItem.objects.get(id=id)
    comments = Comment.objects.filter(auction=item)
    bid = get_object_or_404(Bid, auction=item)
    return render(request, 'auctions/item.html', {
        "item": item,
        "comment_form": form,
        "comments": comments,
        "bid": bid,
        "user": request.user
    })

def add_comment(request, id):
    if request.method == "POST":
        form = CommentForm(request.user, request.POST)
        item = AuctionItem.objects.get(id=id)
        comments = Comment.objects.filter(auction=item)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            comment = Comment(user=request.user,auction=get_object_or_404(AuctionItem, id=id),**cleaned_data)
            comment.save()
            form = CommentForm(request.user)
            return HttpResponseRedirect(reverse('item', kwargs={
                'id': id
            }))
        else:
            return render(request, 'auctions/item.html', {
                "item": item,
                "comment_form": form,
                "comments": comments
            })

def update_bid(request, id):
    amount = request.POST["bid"]
    if amount:
        amount=float(amount)
        auction_item = AuctionItem.objects.get(id=id)
        bid = Bid.objects.get(auction=auction_item)
        if amount > bid.amount:
            bid.user = request.user
            bid.amount = amount
            bid.save()
            auction_item.bid_counter += 1
            auction_item.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            raise ValidationError('Bid must be greater than current Bid value')
    else:
        raise ValidationError('Bid must be greater than current Bid value')
      
def close_bid(request, id):
    auction = get_object_or_404(AuctionItem, id=id)
    auction.active = False 
    auction.winner = request.user.username
    auction.save()
    return HttpResponseRedirect(reverse('home'))



