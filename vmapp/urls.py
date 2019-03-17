from django.urls import path

from . import views

app_name = 'vmapp'
urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('logout/', views.logout),
    path('detail/<str:section>/<str:vm_type>/<str:vm_id>', views.detail),
    path('state/<str:section>/<str:vm_type>/<str:vm_id>', views.state)
]