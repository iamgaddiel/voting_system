from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    Dashboard,
    Index,
    Regisration
)


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    path('register/', Regisration.as_view(), name="registration"),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
]