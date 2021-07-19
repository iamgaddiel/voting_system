from django.urls import path

from .views import (
    JoinPoll,
    ParticipantDashboard,
    ParticipantProfileDetail,
    ParticipantPollsDashboard,
    HandleProjectLinkUpload,
    ParticipantProfileUpdate
)


urlpatterns = [
    path('dahsboard/', ParticipantDashboard.as_view(), name="participant_dashboard"),
    path('profile/', ParticipantProfileDetail.as_view(), name='participant_profile'),
    path('profile/update/', ParticipantProfileUpdate.as_view(), name='participant_profile_update'),
    path('join/poll/', JoinPoll.as_view(), name='particiapant_join_polls'),
    path('dashboard/poll/<poll_address>/', ParticipantPollsDashboard.as_view(), name='participant_poll'),
    path('project/link/upload/', HandleProjectLinkUpload.as_view(), name="participant_link_upload")
]