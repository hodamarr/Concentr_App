from django.urls import path
from . import views

urlpatterns = [
    path("experiments/", views.ExperimentListCreateView.as_view(), name="list_create_experiments"),
    # path(
    #     "<int:pk>/",
    #     views.PostRetrieveUpdateDeleteView.as_view(),
    #     name="post_detail",
    # ),
    path("participants/", views.ParticipantExperimentCreateView.as_view(), name="list_create_participants")
]