from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

import inspect

from .models import User, Message


def index(request, page_number=1):
    
    # Get all messages
    messages = Message.objects.all()
    
    # Paginate
    p = Paginator(messages, 10)
    num_pages = p.num_pages
   
    # Return max 10 messages
    if num_pages > 1:
        messages = p.page(page_number).object_list

    # Check min and max
    previous = page_number - 1
    next = page_number + 1

    return render(request, "network/index.html", {
        "messages": messages,
        "num_pages": num_pages,
        "page_range": p.page_range,
        "curr_page": page_number,
        "previous": previous,
        "next": next
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
    return HttpResponseRedirect(reverse("index"))

def profile(request, name, page_number=1):

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

    num_pages = 0
    page_range = range(0)
    curr_page = 0
    previous = 0
    next = 0

    # Page messages if necessary
    if len(messages) > 10:
        dict = make_pages(messages, page_number)
        messages = dict["messages"]
        num_pages = dict["num_pages"]
        page_range = dict["page_range"]
        curr_page: dict["curr_page"]
        previous = dict["previous"]
        next = dict["next"]


    # Show profile page
    return render(request, "network/profile.html", {
        "is_curr_user": is_curr_user,
        "profile": user,
        "messages": messages,
        "following": following_count,
        "followers": followers_count,
        "is_following": is_following,
        "num_pages": num_pages,
        "page_range": page_range,
        "curr_page": curr_page,
        "previous": previous,
        "next": next
    })

def following(request, page_number=1):
    # get list of following, then get their messages
    following = User.objects.values('following').filter(username=request.user)
    messages = Message.objects.filter(user__in=following)

    num_pages = 0
    page_range = range(0)
    curr_page = 0
    previous = 0
    next = 0

    # Page messages if necessary
    if len(messages) > 10:
        dict = make_pages(messages, page_number)
        messages = dict["messages"]
        num_pages = dict["num_pages"]
        page_range = dict["page_range"]
        curr_page: dict["curr_page"]
        previous = dict["previous"]
        next = dict["next"]

    return render(request, "network/index.html", {
        "messages": messages,
        "num_pages": num_pages,
        "page_range": page_range,
        "curr_page": curr_page,
        "previous": previous,
        "next": next
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

def make_pages(messages, page_number):
    # Paginate
    p = Paginator(messages, 10)
    num_pages = p.num_pages
   
    # Return max 10 messages
    if num_pages > 1:
        messages = p.page(page_number).object_list

    # Check min and max
    previous = page_number - 1
    next = page_number + 1

    # Return values
    return {
        "messages": messages,
        "num_pages": num_pages,
        "page_range": p.page_range,
        "curr_page": page_number,
        "previous": previous,
        "next": next
    }