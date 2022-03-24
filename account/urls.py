from django.contrib import admin
from django.urls import path, include
import account
from .views import RegistrationAPI, UserAPI

urlpatterns = [
    path("auth/register/", RegistrationAPI.as_view()),
    path("auth/user/", UserAPI.as_view()),
]
