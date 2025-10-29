from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]

urlpatterns += [
    path('application/create/', views.create_application, name='create_application'),
    path('application/delete/<int:application_id>/', views.delete_application, name='delete_application'),
]
