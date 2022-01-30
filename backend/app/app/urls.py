"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, re_path
from main.endpoints import LoginEndpoint, RegisterEndpoint
from chess_backend.endpoints import GameEndpoint, AcceptGameInvite
from main.views import Test

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterEndpoint.as_view()),
    path('login/', LoginEndpoint.as_view()),
    path('create-game/', GameEndpoint.as_view()),
    re_path(r'get-game/(?P<game_key>\w+)/$', GameEndpoint.as_view()),
    re_path(r'accept-game/(?P<game_key>\w+)/$', AcceptGameInvite.as_view()),
    path('test/', Test.as_view())
]
