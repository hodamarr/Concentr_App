from rest_framework import serializers
from .models import *


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = ['id', 'created_at', 'updated_at', 'name', 'description']


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'created_at', 'participant_code']


class ParticipantExperimentSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer()
    experiment = ExperimentSerializer()

    class Meta:
        model = ParticipantExperiment
        fields = ['id', 'participant', 'experiment', 'created_at']


class ContextSerializer(serializers.ModelSerializer):
    experiment = ExperimentSerializer()

    class Meta:
        model = Context
        fields = ['id', 'updated_at', 'created_at', 'name', 'description', 'experiment']


class QuestionSerializer(serializers.ModelSerializer):
    context = ContextSerializer()

    class Meta:
        model = Question
        fields = ['id', 'description', 'updated_at', 'created_at', 'context']


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = ['id', 'updated_at', 'created_at', 'text', 'question']