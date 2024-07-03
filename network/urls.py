
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.add_post, name="new_post"),
    path("post/id=<int:post_id>", views.edit_post, name="edit_post"),
    path("profile/<str:username>&id=<int:profile_id>", views.get_profile, name="get_profile"),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("following", views.get_following, name="following_posts"),
    path("like/post_id=<int:post_id>", views.like, name="like"),
]
