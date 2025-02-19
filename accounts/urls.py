from django.urls import path
from . import views
urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('orders/', views.orders, name='accounts.orders'),
    path('reset-password/', views.reset_password_request, name='accounts.reset_password_request'),
    path('reset-password/confirm/', views.reset_password_confirm, name='accounts.reset_password_confirm'),
]