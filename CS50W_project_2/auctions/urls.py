from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register", views.register, name="register"),
    path("signin", views.signin, name="signin"),
    path("logout", views.logout_view, name="logout"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watch/<int:id>", views.add_to_watchlist, name="watch"),
    path("unwatch/<int:id>", views.remove_from_watchlist, name="unwatch"),
    path("item/<int:id>", views.item, name="item"),
    path("categories", views.categories, name="categories"),
    path("categories/<category>", views.category, name="category"),
    path("comment/<int:id>", views.add_comment, name="add_comment"),
    path("update_bid/<int:id>", views.update_bid, name="update_bid"),
    path("close_bid/<int:id>", views.close_bid, name="close_bid")
]