from django.urls import path
from .views import (
    JoinPoll,
    JudgePollDashboard,
    JudgesDashboard
)


urlpatterns = [
    path('dashboard/', JudgesDashboard.as_view(), name="judges_dashboard"),
    path('dashboard/poll/<poll_address>/', JudgePollDashboard.as_view(), name='judges_poll_dashboard'),
    path('join/poll/', JoinPoll.as_view(), name='judges_join_poll'),
]