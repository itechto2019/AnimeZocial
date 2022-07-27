from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexPage, name="index"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),

    path('create-feed/', views.createFeed, name="create-feed"),
    path('update-feed/<str:id>/', views.updateFeed, name="update-feed"),
    path('delete-feed/<str:id>/', views.deleteFeed, name="delete-feed"),
    
    path('profile/<str:username>/', views.profilePage, name="profile-info"),
    path('profile/edit', views.profileUpdate, name="profile-edit"),
    path('profile/change-password', views.changePassword, name="change-password"),

    path('like-feed/<str:id>/', views.likeFeed, name="like-feed"),
    path('feed/<str:user>/<str:topic>/<str:id>/', views.feed, name="feed"),
]