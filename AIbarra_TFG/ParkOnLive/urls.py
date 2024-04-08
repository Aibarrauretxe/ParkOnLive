from django.urls import path

from .home import views as home_views
from .users import views as user_views

urlpatterns = [
    path("", home_views.home, name="home_view"),
    path("login", user_views.login, name="login_view"),
    path("logout", user_views.logout, name="logout_view"),
    path("user_signup", user_views.user_signup, name="user_signup_view"),
    path("provider_signup", user_views.provider_signup, name="provider_signup_view"),
    path("profile", user_views.profile, name="profile_view"),
    path("parking_create", home_views.parking_create, name="parking_create_view"),
    path("parkings_provider", home_views.parkings_provider, name="parkings_provider_view"),
    path("edit_parking/<int:pk>/", home_views.edit_parking, name="edit_parking"),
    path("delete_parking/<int:pk>/", home_views.delete_parking, name="delete_parking"),
    path("parkings/", home_views.parkings, name="parkings"),
    path("toggle_favorite/<int:pk>/", home_views.toggle_favorite, name="toggle_favorite"),
    path("register_occupancy/", home_views.register_occupancy, name="register_occupancy")
]