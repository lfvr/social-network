
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:page_number>", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<str:name>", views.profile, name="profile"),
    path("profile/<str:name>/<int:page_number>", views.profile, name="profile"),
    path("follow", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("following/<int:page_number>", views.following, name="following"),
    path("edit/<int:message_id>", views.edit, name="edit"),
    path("like/<int:message_id>/<incr>", views.like, name="like")
]
