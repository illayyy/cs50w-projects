
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<int:profile_id>", views.profile_view, name="profile"),
    path("following", views.following_view, name="following"),

    path("follow/<int:profile_id>", views.follow, name="follow"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("like/<int:post_id>", views.like, name="like"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
