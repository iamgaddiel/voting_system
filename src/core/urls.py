from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.urls.conf import include
from .views import (
    Index,
    Dispacther,
    Regisration
)


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    path('login/dispatcher/', Dispacther.as_view(), name="dispatcher"),
    path('registration/', Regisration.as_view(), name="registration"),

    # other apps
    path('participants/en/', include('participants.urls')),
    path('judges/en/', include('judges.urls')),
]