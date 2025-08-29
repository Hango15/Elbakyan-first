from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.handle_search, name='handle_search'),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("shop/", views.shop, name="shop"),
    path("product/<int:id>/", views.product_details, name="product_details"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path('contact/', views.contact_view, name='contact'),
    path("add-game/", views.add_game, name="add_game"),
    path("game/<int:id>/edit/", views.edit_game, name="edit_game"),
    path("game/<int:id>/delete/", views.delete_game, name="delete_game"),
]
