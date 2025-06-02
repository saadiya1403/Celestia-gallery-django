from django.urls import path
from .views import HomePageView, CreatePost, post_detail, color_palette # new
from . import views

urlpatterns = [
    path("", HomePageView, name="home"), # see all post
    path("post/", CreatePost, name="add_post"), # add new post
    path("post/<int:post_id>/", post_detail, name="post_details"), # view a post
    path("post/like_post/", views.add_like, name="like_post"),
    path("color_palette/", color_palette, name="color_palette")
]