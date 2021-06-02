from django.urls import path

from .views import (
    JoinPoll,
    ParticipantDashboard,
    ParticipantProfileDetail,
    ParticipantPollsDashboard,
)


urlpatterns = [
    path('dahsboard/', ParticipantDashboard.as_view(), name="participant_dashboard"),
    path('profile/', ParticipantProfileDetail.as_view(), name='participant_profile'),
    path('join/poll/', JoinPoll.as_view(), name='particiapant_join_polls'),
    path('dashboard/poll/<poll_address>/', ParticipantPollsDashboard.as_view(), name='participant_poll')

]