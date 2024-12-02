"""
URL configuration for authentication project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from main_app.views import *


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", login_view, name="login"),
    path("logout/", custom_logout_view, name="logout"),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("home/", home, name="home"),
    path("register/", register_user, name="register"),
    path("verify/<int:user_id>/<str:otp>/", verify_email, name="verify_email"),
    path('phone_register/', phone_number_register, name='phone_number_register'),
    path('verify_phone_otp/<int:user_id>/', verify_phone_otp, name='verify_phone_otp'),
    path("phone_login/", phone_login, name="phone_login"),
    path('verify_phone_login_otp/<int:user_id>/', verify_phone_login_otp, name='verify_phone_login_otp'),
    
]
