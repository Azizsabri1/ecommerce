# accounts/urls.py
from django.urls import path

from store.views import my_orders
from . import views
from .views import manage_users, edit_user, delete_user

urlpatterns = [
    path('auth/', views.auth_page, name='auth'),  # ← nouvelle route
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.client_dashboard, name='client_dashboard'),
    path("profile/", views.profile_view, name="profile"),
    path('orders/', my_orders, name='my_orders'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/manage-users/', manage_users, name='manage_users'),
    path('admin/users/edit/<int:user_id>/', edit_user, name='edit_user'),
    path('admin/users/delete/<int:user_id>/', delete_user, name='delete_user'),


]
