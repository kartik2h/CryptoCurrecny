from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutView, name="logout"),
    path('home/', views.index, name='index'),
    #path('index1/', views.index1, name='index1'),
    path('blockchain/', views.blockchain, name='blockchain'),
    path('Markettrends/', views.Markettrends, name='Markettrends'),
    path('crypto/<str:symbol>/', views.crypto_detail, name='crypto_detail'),
    path('technology/', views.tech_view, name='tech_page'),
    path('investment/', views.invest_view, name='invest'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

