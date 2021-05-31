from django.urls import path
from .views import (
    JudgesDashboard
)


urlpatterns = [
    path('dashboard/', JudgesDashboard.as_view(), name="judges_dashboard")
]