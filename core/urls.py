from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutView, name="logout"),
    path('home/', views.index, name='index'),
    path('blockchain/', views.blockchain, name='blockchain'),
    path('Markettrends/', views.Markettrends, name='Markettrends'),
]
