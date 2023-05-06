from rest_framework import generics, mixins, status
import random as r
import string
from .serializers import *
from rest_framework.permissions import (
    IsAuthenticated,
    BasePermission,
)
from rest_framework.request import Request
from rest_framework.response import Response


class IsExperimentAdminPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.exp_admin == request.user


class ExperimentListCreateView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = ExperimentSerializer
    queryset = Experiment.objects.all()
    permission_classes = [IsAuthenticated, IsExperimentAdminPermission]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(exp_admin=user)
        return super().perform_create(serializer)

    def get(self, request: Request, *args, **kwargs):
        user_id = request.user.id
        # Retrieve all experiments for the user with the given user ID
        experiments = Experiment.objects.filter(exp_admin=user_id)
        # Serialize the experiments
        experiment_data = ExperimentSerializer(experiments, many=True).data
        return Response(experiment_data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ContextCreateView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = ContextSerializer
    permission_classes = [IsAuthenticated, IsExperimentAdminPermission]

    def post(self, request):
        experiment_name = request.data.get('experiment')
        try:
            experiment = Experiment.objects.get(name=experiment_name)
        except Experiment.DoesNotExist:
            return Response({'error': 'Experiment not found.'},
                            status=status.HTTP_404_NOT_FOUND)
        name = request.data.get('name')
        description = request.data.get('description')
        context = Context.objects.create(
            name=name,
            description=description,
            experiment=experiment
        )
        context.save()
        serializer = self.serializer_class(context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get(self, request):
        experiment_name = request.headers.get('experiment')
        try:
            experiment = Experiment.objects.get(name=experiment_name)
            data = Context.objects.filter(experiment=experiment)
        except Experiment.DoesNotExist as e:
            return Response({"message": "Experiment does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Context.DoesNotExist as e:
            return Response({"message": "context does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": "sucess",
             "data": [{"name": item.name, "description": item.description} for item in data]},
            status=status.HTTP_201_CREATED)

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
        return Response({'message': 'success', 'data': participants}, status.HTTP_200_OK)


class QuestionCreateList(generics.GenericAPIView,
                                      mixins.CreateModelMixin):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsExperimentAdminPermission]

    def get(self, request):
        experiment_name = request.headers.get('experiment')
        context_name = request.headers.get('context')
        try:
            experiment = Experiment.objects.get(name=experiment_name)
            context = Context.objects.get(name=context_name, experiment=experiment)
        except Context.DoesNotExists as e:
            return Response({'error': 'context not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Experiment.DoesNotExists as e:
            return Response({'error': 'experiment not found.'}, status=status.HTTP_404_NOT_FOUND)
        questions = Question.objects.filter(context=context)
        return Response({'message': 'success', 'data': [{'id': i.id, 'description': i.description,
                                                         'answers':[j.text for j in Answer.objects.filter(question=i)]} for i in questions]},
                        status=status.HTTP_200_OK)

    def post(self, request):
        try:
            experiment_name = request.data.get('experiment')
            context_name = request.data.get('context')
            description = request.data.get('description')
            experiment = Experiment.objects.get(name=experiment_name)
            context = Context.objects.get(name=context_name, experiment=experiment)
        except Context.DoesNotExists as e:
            return Response({'error': 'context not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Experiment.DoesNotExists as e:
            return Response({'error': 'experiment not found.'}, status=status.HTTP_404_NOT_FOUND)

        question = Question.objects.create(context=context, description=description)
        question.save()
        serializer = self.serializer_class(question)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AnswerCreateListView(generics.GenericAPIView,
                                      mixins.CreateModelMixin):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, IsExperimentAdminPermission]

    def post(self, request):
        try:
            question_id = request.data.get('question_id')
            text = request.data.get('text')
            question = Question.objects.filter(id=question_id)[0]
            answer = Answer.objects.create(
                text=text,
                question=question,
            )
            answer.save()
            serializer = self.serializer_class(answer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Question.DoesNotExist as e:
            return Response({'error': 'question not found'}, status=status.HTTP_404_NOT_FOUND)
