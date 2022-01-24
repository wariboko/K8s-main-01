from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('createListing', views.createListing, name='createListing'),
   path("categoryList/<str:category_id>", views.categoryList, name='categoryList'),
   path("addWatchlist/<int:auction_id>", views.addWatchlist, name="addWatchlist"),
   path("watchlist", views.watchlist, name="watchlist"),
   path("remove_watchlist/<int:auction_id>", views.remove_watchlist, name="remove_watchlist"),
   path("indexItem/<int:auction_id>", views.indexItem, name="indexItem"),
   path('PostImage/<int:auction_id>', views.PostImage, name="PostImage")
   
]
