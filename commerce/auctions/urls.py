from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("chooseCategory", views.chooseCategory, name="chooseCategory"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("removeWatchList/<int:id>", views.removeWatchList, name="removeWatchList"),
    path("addWatchList/<int:id>", views.addWatchList, name="addWatchList"),
    path("WatchList", views.WatchList, name="WatchList"),
    path("addComments/<int:id>", views.addComments, name="addComments"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("listing/<int:id>/close", views.close, name="close")
]
