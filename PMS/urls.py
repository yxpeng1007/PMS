"""
URL configuration for PMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from app01 import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path(
        "forgot_password_phone/",
        views.forgot_password_phone,
        name="forgot_password_phone",
    ),
    path("reset_password/", views.reset_password, name="reset_password"),
    path("home/", views.home, name="home"),
    path(
        "forgot_password/check/",
        views.forgot_password_check,
        name="forgot_password_check",
    ),
    path(
        "forgot_password_phone/check/",
        views.forgot_password_phone_check,
        name="forgot_password_phone_check",
    ),
]
