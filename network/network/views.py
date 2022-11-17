import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


def paginate(items, request):
    items = items.order_by("-timestamp")

    paginator = Paginator(items, 10)
    page_number = request.GET.get("page")
    if page_number is None:
        page_number = 1
    page_object = paginator.get_page(page_number)

    return page_object


def index(request):
    if request.method == "POST":
        new_post(request)

    posts = Post.objects.all()
    page_object = paginate(posts, request)

    return render(request, "network/index.html", {
        'page_object': page_object,
        'title': "All Posts"
    })


def new_post(request):
    creator = request.user
    content = request.POST.get("content")
    post = Post.objects.create(
        creator=creator,
        content=content
    )
    post.save()


def profile_view(request, profile_id):
    profile = User.objects.get(pk=profile_id)
    posts = profile.user_posts.all()
    page_object = paginate(posts, request)

    followers = profile.user_followers.all()
    if request.user in followers:
        follow_button_content = "Unfollow"
    else:
        follow_button_content = "Follow"
    followers_count = followers.count()
    following_count = profile.following.all().count()

    return render(request, "network/profile.html", {
        'profile': profile,
        'page_object': page_object,
        'follow_button_content': follow_button_content,
        'followers_count': followers_count,
        'following_count': following_count,
    })


def following_view(request):
    if request.user.is_authenticated:
        following = User.objects.get(pk=request.user.id).following.all()
        if following:
            posts = following[0].user_posts.all()
            for profile in following[1:]:
                posts = posts | profile.user_posts.all()

            page_object = paginate(posts, request)
        else:
            page_object = []

        return render(request, "network/index.html", {
            'page_object': page_object,
            'title': "Following"
        })
    else:
        return redirect('index')


def follow(request, profile_id):
    profile = User.objects.get(pk=profile_id)
    user = request.user
    if user in profile.user_followers.all():
        profile.user_followers.remove(user)
        return HttpResponse('unfollowed')
    else:
        profile.user_followers.add(user)
        return HttpResponse('followed')


@csrf_exempt
def edit(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user.id == post.creator.id:
        data = json.loads(request.body)
        post.content = data['content']
        post.save()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=403)


def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        return HttpResponse('unliked')
    else:
        post.likes.add(user)
        return HttpResponse('liked')


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
