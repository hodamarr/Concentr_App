from django.urls import path
from . import views

urlpatterns = [
    path(
        "experiments/",
        views.ExperimentListCreateView.as_view(),
        name="list_create_experiments"),
    path('experiments/<int:pk>/', views.ExperimentListCreateView.as_view(), name='experiment-delete-update'),

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
        "question/<int:pk>/",
        views.QuestionCreateList.as_view(),
        name="question-delete-update"),
    path(
        'answer/',
        views.AnswerCreateListView.as_view(),
        name="list_create_answer"),
    path(
        "answer/<int:pk>/",
        views.AnswerCreateListView.as_view(),
        name="answer-delete-update"),
    path(
        'submission/',
        views.ParticipantSubmissionView.as_view(),
        name="participant_submission"),
    path(
        'participantlogin/',
        views.ParticipantLoginView.as_view(),
        name="participant_login"),
    path(
        "participantlogin/<str:pk>/",
        views.ParticipantLoginView.as_view(),
        name="participant_login_update"),
    path(
        'scheduler/',
        views.ScheduleListView.as_view(),
        name="schedule"),
    path(
        'questionsforparticipant/',
        views.QuestionForParticipantsListView.as_view(),
        name='question_for_participant'
    ),
    path(
        'submission/data/',
        views.PartipantSubmissionGet.as_view(),
        name='submission_get'
    )
    # path(
    #     'submission/',
    #     views.SubmittionPost.as_view(),
    #     name='submission_data'
    # ),

]
