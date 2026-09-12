from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('history/', views.history, name='history'),
    path('api/shorten/', views.shorten_url, name='shorten_url'),
    path('api/history/', views.url_history, name='url_history'),
    path('<str:short_code>/', views.redirect_url, name='redirect_url'),
]
