"""SoftDesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import SignupView
from projects.views import ProjectListApiView
from rest_framework import routers



projects_router = routers.SimpleRouter()
projects_router.register('projects', ProjectListApiView, basename='projects')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup', SignupView.as_view(), name='register'),
    path('accounts/login', TokenObtainPairView.as_view(), name='register'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/', include(projects_router.urls)),

   
]
