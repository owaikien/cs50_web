from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import User, Posts, Profile
from django.core.paginator import Paginator
from django import template

def index(request):
    posts = Posts.objects.all().order_by("-timestamp")

    # paginator
    paginator = Paginator(posts, 10)

    print(paginator.count)
    print(paginator.num_pages)
    # get page number
    page_number = request.GET.get('page')

    # use paginator `get_page`
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj,
    })

@csrf_exempt
@login_required
def new_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post = Posts.objects.create(user = request.user, content = data.get('content'))
        return JsonResponse({'message': 'Post created successfully.'}, status=201)

def all_posts(request):
    posts = Posts.objects.all().order_by('-timestamp')
    return render(request, "network/index.html", {
        "posts": posts,
    })

# Create a view for the profile page
def profile(request, username):
    profile_user = User.objects.get(username=username)
    profile = Profile.objects.get(user=profile_user)
    posts = Posts.objects.filter(user=profile_user).order_by("-timestamp")
    logged_in_user_profile = Profile.objects.get(user=request.user)
    is_following = profile in logged_in_user_profile.follows.all()
    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        'profile': profile,
        'posts': posts,
        'is_following': is_following
    })

@login_required
def follow(request, username):
    if request.method == "POST":
        profile_user = User.objects.get(username=username)
        profile = Profile.objects.get(user=profile_user)
        logged_in_user_profile = Profile.objects.get(user=request.user)
        if profile in logged_in_user_profile.follows.all():
            logged_in_user_profile.follows.remove(profile)
        else:
            logged_in_user_profile.follows.add(profile)

        return HttpResponseRedirect(reverse('profile', args=(username, )))

@login_required
def following(request, username):
    # Get profile of current user 
    user_profile = Profile.objects.get(user=request.user)

    # Get all followings of the profile 
    followed_profiles = user_profile.follows.all()

    # Get the user object of all followed_users
    followed_users = [profile.user for profile in followed_profiles]

    # Screen
    posts = Posts.objects.filter(user__in=followed_users).order_by("-timestamp")

    # Post Render
    return render(request, "network/following.html", {
        "posts": posts,
    })

@csrf_exempt
def like(request, post_id):
    print(f"Like request received for post_id: {post_id}")
    try:
        post = Posts.objects.get(id=post_id)
        if request.method == "PUT":
            data = json.loads(request.body)
            print(f"Request data: {data}")
            if data.get('like') is True:
                post.likes.add(request.user)
            else:
                post.likes.remove(request.user)
            post.save()
            return JsonResponse({"likes": post.likes.count()}, safe=False)
    except Exception as e:
        print(f"Error handling like request: {e}")
        return JsonResponse({"error": str(e)}, status=400)

    

@login_required
@csrf_exempt
def edit_post(request, post_id):
    try:
        post = Posts.objects.get(id=post_id)

        if request.method == "POST":
            # Get the new content
            data = json.loads(request.body)
            new_content = data.get("content")

            # Update and save the post
            post.content = new_content
            post.save()

            return JsonResponse(post.serialize(), safe=False)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)



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

        # Attempt to create new user and profile
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            # Create profile
            profile = Profile.objects.create(user=user)
            profile.save()

        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
