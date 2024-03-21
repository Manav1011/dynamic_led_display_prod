from django.urls import path
from .views import LoginView,LogoutView,RegisterView

urlpatterns = [
    path('login/',LoginView,name='login'),
    path('logout/',LogoutView,name='logout'),
    path('register/',RegisterView,name='register')
]
