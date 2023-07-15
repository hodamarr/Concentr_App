from rest_framework import serializers
from .models import *


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = ['id', 'created_at', 'updated_at', 'name', 'description']


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'created_at', 'participant_code', 'expo_token', 'is_female']


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
        fields = [
            'id',
            'updated_at',
            'created_at',
            'name',
            'description',
            'experiment']


class QuestionSerializer(serializers.ModelSerializer):
    context = ContextSerializer()

    class Meta:
        model = Question
        fields = ['id', 'description', 'updated_at', 'created_at', 'context', 'related_answer', 'parent_id']


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = ['id', 'updated_at', 'created_at', 'text', 'question']


class ParticipantSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantSubmission
        fields = [
            'id',
            'created_at',
            'updated_at',
            'participant',
            'context',
            'question',
            'answer']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ScheduleSerializer(serializers.ModelSerializer):
    participant_code = serializers.CharField(source='participant.participant_code')

    class Meta:
        model = Schedule
        fields = ('ping_times', 'participant_code', 'experiment', 'context')
