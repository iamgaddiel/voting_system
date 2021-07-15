from django.urls import path
from .views import (
    GetParticipantDetail,
    JoinPoll,
    JudgePollDashboard,
    JudgesDashboardIndex,
    VoteParticipant,
    GetRanking,
    JudgesProfileDashboard,
    JudgesProfileUpdate
)


urlpatterns = [
    path('dashboard/', JudgesDashboardIndex.as_view(), name="judges_dashboard"),
    path('profile/', JudgesProfileDashboard.as_view(), name="judges_profile"),
    path('profile/update/', JudgesProfileUpdate.as_view(), name="judges_profile_update"),
    path('dashboard/poll/<poll_address>/', JudgePollDashboard.as_view(), name='judges_poll_dashboard'),
    path('join/poll/', JoinPoll.as_view(), name='judges_join_poll'),
    path('get/participant/detail/<id>/<poll_address>/', GetParticipantDetail.as_view(), name="judge_participant_detail"),
    path('vote/participant/', VoteParticipant.as_view(), name="judge__vote_participant"),
    path('get/participant/rankings/<address>/', GetRanking.as_view(), name="judge__rating"),
]