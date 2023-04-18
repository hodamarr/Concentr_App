from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status
from rest_framework.decorators import APIView, api_view, permission_classes
from .models import *
import random as r
import string
from .serializers import *
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser, BasePermission,
)
from rest_framework.request import Request
from rest_framework.response import Response



class IsExperimentAdminPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.exp_admin == request.user


class ExperimentListCreateView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = ExperimentSerializer
    queryset = Experiment.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(exp_admin=user)
        return super().perform_create(serializer)

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ParticipantExperimentCreateView(generics.GenericAPIView,
                                      mixins.CreateModelMixin):
    serializer_class = ParticipantExperimentSerializer
    permission_classes = [IsAuthenticated, IsExperimentAdminPermission]

    def post(self, request, *args, **kwargs):
        experiment_name = request.data.get('experiment')
        try:
            experiment = Experiment.objects.get(name=experiment_name)
        except Experiment.DoesNotExist:
            return Response({'error': 'Experiment not found.'},
                            status=status.HTTP_404_NOT_FOUND)
        # todo - if the code already exists.
        participant_code = ''.join(r.choices(string.ascii_letters + string.digits, k=8))
        participant = Participant.objects.create(participant_code=participant_code)
        participant.save()

        participant_experiment = ParticipantExperiment.objects.create(
            participant=participant,
            experiment=experiment,
        )
        participant_experiment.save()
        # todo: change to retun only {"paticipant_code": "blabla", "experiment": "blabla"}
        serializer = self.serializer_class(participant_experiment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        experiment_name = request.GET.get('experiment')
        try:
            experiment = Experiment.objects.get(name=experiment_name)
        except Experiment.DoesNotExists:
            return Response({'error': 'Experiment not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        experiment_participants = ParticipantExperiment.objects.filter(experiment=experiment)
        participants = [i.participant.participant_code for i in experiment_participants]
        return Response({'participants': participants}, status.HTTP_200_OK)

