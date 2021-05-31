from django.urls import path

from .views import (
    ParticipantDashboard,
    ParticipantProfileDetail,
)


urlpatterns = [
    path('dahsboard/', ParticipantDashboard.as_view(), name="participant_dashboard"),
    path('profile/', ParticipantProfileDetail.as_view(), name='participant_profile'),

]