from django.urls import path
from . import views

urlpatterns = [
    path(
        "experiments/",
        views.ExperimentListCreateView.as_view(),
        name="list_create_experiments"),
    # path(
    #     "<int:pk>/",
    #     views.PostRetrieveUpdateDeleteView.as_view(),
    #     name="post_detail",
    # ),
    path(
        "participants/",
        views.ParticipantExperimentCreateView.as_view(),
        name="list_create_participants"),
    path(
        "context/",
        views.ContextCreateView.as_view(),
        name="list_create_contexts"),
    path(
        "question/",
        views.QuestionCreateList.as_view(),
        name="list_create_questions"),
    path(
        'answer/',
        views.AnswerCreateListView.as_view(),
        name="list_create_answer"),
    path(
        'submission/',
        views.ParticipantSubmissionView.as_view(),
        name="participant_submission"),
    path(
        'participantlogin/',
        views.ParticipantLoginView.as_view(),
        name="participant_login"),
    path(
        'scheduler/',
        views.ScheduleListView.as_view(),
        name="schedule"),


]
