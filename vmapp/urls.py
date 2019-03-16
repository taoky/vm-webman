from django.urls import path

from . import views

app_name = 'vmapp'
urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('logout/', views.logout),
]