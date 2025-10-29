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

urlpatterns += [
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/application/change-status/<int:application_id>/', views.change_application_status, name='change_application_status'),
    path('admin/categories/', views.manage_categories, name='manage_categories'),
    path('admin/categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
]