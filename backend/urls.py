"""toastmasters URL Configuration

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
from django.urls import include, path

from rest_framework import routers

from .moderator import views


router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('api/login', views.login),
    path('api/meeting_update', views.meeting_update),
    path('api/meeting', views.meeting),
    path('api/speaker', views.speaker),
    path('api/speakers', views.speakers),
    path('api/feedback_update', views.feedback_update),
    path('api/feedback', views.feedback),
    path('api/feedback_pdf', views.feedback_pdf),
    path('api/voting', views.voting),
    path('api/voting_update', views.voting_update),
    path('api/remove', views.remove),
    path('api/test', views.test),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework"))
]