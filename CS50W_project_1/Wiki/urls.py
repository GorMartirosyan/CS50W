from django.urls import path
from . import views

app_name='wiki'
urlpatterns = [
    path("", views.home, name="home"),
    path("new-page", views.new_page, name="create_new_page"),
    path("<element>", views.page_details, name="details"),
    path("pages/random", views.open_random_page, name="random"),
    path("<element>/delete", views.delete_page, name="delete"),
    path("<element>/edit", views.edit_page, name="edit"),
    path('search/', views.search_view, name='search')
]