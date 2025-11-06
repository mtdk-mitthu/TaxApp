from django.contrib import admin
from django.urls import path

# 1. Import ALL your views from your taxapp
from taxapp.views import (
    homepage_view, 
    register, 
    user_login, 
    user_logout, 
    dashboard
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # 2. Connect each path to its view function
    path('', homepage_view, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
]