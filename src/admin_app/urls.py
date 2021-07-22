from django.urls import path
from django.views.generic.list import ListView
from .views import (
    # polls
    AdminDashboard,
    ListPoll,
    CreatePoll,
    DeleteAllPolls,
    DeleteSinglePoll,
    UpdatePoll,
    GetPoll,

    # participant
    ListParticipants,
    GetParticipant,
    DeleteParticipant,

    # jugdes
    ListJudges,
    GetJudge,
    DeleteJudge,
    CreateJudge,

    # admins
    ListAdmin,
    GetAdmin,
    DeleteAdmin,
    CreateAdmin
)


urlpatterns = [
    path('dashboard', AdminDashboard.as_view(), name="admin_dashboard"),
    path('polls', ListPoll.as_view(), name="admin_polls_list"),
    path('polls/create/', CreatePoll.as_view(), name="admin_polls_create"),
    path('polls/delete/', DeleteAllPolls.as_view(), name="admin_polls_delete"),
    path('polls/delete/<int:pk>/', DeleteSinglePoll.as_view(), name="admin_delete_all_polls"),
    path('polls/update/<int:pk>/', UpdatePoll.as_view(), name="admin_update_polls"),
    path('polls/get/<pk>/', GetPoll.as_view(), name="admin_polls_detail"),

    # ================== [participants] ==============================
    path('participants/list/', ListParticipants.as_view(), name="admin_participants_list"),
    path('participants/get/<id>/', GetParticipant.as_view(), name="admin_participants_detail"),
    path('participants/get/<id>/delete', DeleteParticipant.as_view(), name="admin_participants_delete"),

    # ================== [judges] ==============================
    path('judges/list/', ListJudges.as_view(), name="admin_judges_list"),
    path('judge/get/<id>/', GetJudge.as_view(), name="admin_judge_detail"),
    path('judge/get/<id>/delete', DeleteJudge.as_view(), name="admin_judge_delete"),
    path('judge/create/', CreateJudge.as_view(), name="admin_judge_create"),

    # ================== [Admmin]] ==============================
    path('admin/users/list/', ListAdmin.as_view(), name="admin_user_list"),
    path('admin/users/get/<pk>/', GetAdmin.as_view(), name="admin_user_get"),
    path('admin/users/delete/<pk>/', DeleteAdmin.as_view(), name="admin_user_delete"),
    path('admin/users/create/', CreateAdmin.as_view(), name="admin_user_create"),
]
