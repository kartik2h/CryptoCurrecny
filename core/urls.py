from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .views import feedback_view

urlpatterns = [
    path('', views.home_view, name='home'),
    
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutView, name="logout"),
    path('home/', views.index, name='index'),
    path('checkout/', views.checkout, name='checkout'),
    path('store/', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    #path('orderhistory/', views.orderhistory, name='orderhistory'),
    #path('index1/', views.index1, name='index1'),
     # Forgot password
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='core/reset_password.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='core/reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='core/reset_password_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='core/reset_password_complete.html'), name='password_reset_complete'),
    path('contact/', views.contact_us, name='contact_us'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('blockchain/', views.blockchain, name='blockchain'),
    path('Markettrends/', views.Markettrends, name='Markettrends'),
    path('crypto/<str:symbol>/', views.crypto_detail, name='crypto_detail'),
    path('technology/', views.tech_view, name='tech_page'),
    path('investment/', views.invest_view, name='invest'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('orderhistory/', views.orderhistory, name='order_history'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

