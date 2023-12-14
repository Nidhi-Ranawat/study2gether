from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("profile/<str:pk>", views.userProfile, name="user-profile"),

    path("", views.home, name="home"),
    path("room/<int:pk>", views.room, name="room"),

    path("create-room", views.create_room, name="create-room"),
    path("update-room/<int:pk>", views.updateRoom, name="update-room"),
    path("del-room/<int:pk>", views.del_room, name="del-room"),
    path("del-msg/<int:pk>", views.del_msg, name="del-msg"),
    path("update-user/", views.updateUser, name="update-user"),
    path("topics/", views.topicsPage, name="topics"),
    path("activity/", views.activityPage, name="activity"),
]
