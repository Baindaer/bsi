"""
URL configuration for bsi project.

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
from ctt.views import login_view, home_view, training_view 
from ctt.views import tactic_form,game_form,session_form,stats_view, delete_training
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('training/',training_view, name='training'),
    path('training/tactic/', tactic_form, name='tactic_form'),
    path('training/game/', game_form, name='game_form'),
    path('training/session/', session_form, name='session_form'),
    path('delete_training/', delete_training, name='delete_training'),
    path('stats/',stats_view, name='stats'),
]
