from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
import json

from .models import User, Posts, Follows, Likes


def index(request):
    posts = Posts.objects.all().order_by("-date")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts_in_a_page = paginator.get_page(page_number)

    liked_posts = []
    try:
        for post in posts_in_a_page:
            if Likes.objects.filter(user=request.user, post=post).exists():
                liked_posts.append(post.id)
            else:
                pass
    except:
        pass

    return render(request, "network/index.html", {
        "title": "All Posts",
        "posts": posts_in_a_page,
        "liked_posts": liked_posts,
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


def add_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        user = User.objects.get(id=request.user.id)
        new_post = Posts(
            user = request.user,
            content = content
        )
        new_post.save()
        return HttpResponseRedirect(reverse("get_profile", kwargs={"profile_id": request.user.id, "username": request.user.username}))

def edit_post(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data["content"]
        post = Posts.objects.get(id=post_id)
        post.content = content
        post.edited = True
        post.save()

        return JsonResponse({"message": f"post: {post_id} edited successfully"}, status=201)

def get_profile(request, profile_id, username):
    user = User.objects.get(id=profile_id)
    following = Follows.objects.filter(user=user)
    followers = Follows.objects.filter(following=user)

    posts = Posts.objects.filter(user=user).order_by("-date")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts_in_a_page = paginator.get_page(page_number)

    liked_posts = []
    for post in posts_in_a_page:
        if Likes.objects.filter(user=request.user, post=post).exists():
            liked_posts.append(post.id)
        else:
            pass
    
    if Follows.objects.filter(user=request.user, following=user).exists():
        is_following = True
    else:
        is_following = False
    
    return render(request, "network/profile.html", {
        "username": username,
        "followers": followers,
        "followings": following,
        "posts": posts_in_a_page,
        "liked_posts": liked_posts,
        "is_following": is_following,
    })

def follow(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        following = User.objects.get(username=request.POST["follow"])
        new_follow = Follows(
            user = user,
            following = following
        )
        new_follow.save()
        return HttpResponseRedirect(reverse("get_profile", kwargs={"profile_id": following.id, "username": following.username}))

def unfollow(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        following = User.objects.get(username=request.POST["unfollow"])
        Follows.objects.filter(user=user, following=following).delete()
        return HttpResponseRedirect(reverse("get_profile", kwargs={"profile_id": following.id, "username": following.username}))

def get_following(request):
    total_following = Follows.objects.filter(user=request.user)
    total_posts = Posts.objects.all().order_by("-date")
    
    posts = []
    for post in total_posts:
        for follows in total_following:
            if follows.following == post.user:
                posts.append(post)

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts_in_a_page = paginator.get_page(page_number)

    liked_posts = []
    for post in posts_in_a_page:
        if Likes.objects.filter(user=request.user, post=post).exists():
            liked_posts.append(post.id)
        else:
            pass

    return render(request, "network/following.html", {
        "title": "Following",
        "posts": posts_in_a_page,
        "liked_posts": liked_posts
    })

def like(request, post_id):
    # if request.method == "POST":
        post = Posts.objects.get(id=post_id)
        if Likes.objects.filter(user=request.user, post=post).exists():
            post.likes -= 1
            post.save()
            Likes.objects.filter(user=request.user, post=post).delete()
            return JsonResponse({"message": f"post: {post_id} unliked successfully", "likes": post.likes, "unlike": True}, status=201)
        else:
            post.likes += 1
            post.save()
            new_like = Likes(
                user = request.user,
                post = post
            )
            new_like.save()
            return JsonResponse({"message": f"post: {post_id} liked successfully", "likes": post.likes, "like": True}, status=201)
