from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.db import IntegrityError

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return render(request, "mail/home.html", {
            "email" : request.user.email
        })
    else:
        return HttpResponseRedirect(reverse("login"))
    
def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "mail/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "mail/login.html")

def register(request):
    if request.method == "GET":
        return render(request, 'mail/register.html')
    else:
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirm_password"]
        if password != confirmation:
            return render(request, "mail/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError:
            return render(request, "mail/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("home"))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))