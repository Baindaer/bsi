from django.urls import path
from .views import LoginView, hola_mundo

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('hola/', hola_mundo, name='hola_mundo'),
]

