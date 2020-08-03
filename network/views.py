from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Message


def index(request):
    return render(request, "network/index.html", {
        "messages": Message.objects.all()
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def new_post(request):
    
    # Make post
    message = request.POST["message"]
    user = request.user
    Message.objects.create(user=user, message=message)

    # Return to posts
    return render(request, "network/index.html", {
        "messages": Message.objects.all()
    })

def profile(request, name):

    # Get user, messages and follow counts
    curr_user = request.user
    user = User.objects.get(username=name)
    messages = Message.objects.filter(user=user)
    following_count = user.following.count()
    followers_count = user.followers.count()

    # Check if current user
    is_curr_user = (curr_user == user)

    # Check if currently following
    is_following = User.objects.filter(username=curr_user.username, following__username=user).exists()

    # Show profile page
    return render(request, "network/profile.html", {
        "is_curr_user": is_curr_user,
        "profile": user,
        "messages": messages,
        "following": following_count,
        "followers": followers_count,
        "is_following": is_following
    })

def following(request):
    # get list of following, then get their messages
    following = User.objects.values('following').filter(username=request.user)
    messages = Message.objects.filter(user__in=following)
    return render(request, "network/index.html", {
        "messages": messages
    })

def follow(request):
    # Get current profile
    profile_name = request.POST["profile"]
    profile = User.objects.get(username=profile_name)

    # Check current status and get current user
    is_following = request.POST["is_following"]
    curr_user = User.objects.get(username=request.user.username)
    if is_following == "true":
        # unfollow
        curr_user.following.remove(profile)
    else: 
        # follow
        curr_user.following.add(profile)
    return JsonResponse({"success": True})

