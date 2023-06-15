
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.new_post, name="newpost"),
    path("allpost", views.all_posts, name="allposts"),
    path("profile/<str:username>", views.profile, name='profile'),
    path('follow/<str:username>', views.follow, name='follow'),
    path('following/<str:username>', views.following, name='following'),
    path('edit_post/<int:post_id>', views.edit_post, name='editpost'),
    path('like/<int:post_id>', views.like, name='like')
]
