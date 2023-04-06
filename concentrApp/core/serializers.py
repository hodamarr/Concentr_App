'''serializers'''
from rest_framework import serializers
from core.models import Experiment, Participant, Question, QuestionAnswer, Context, ContextQuestion, ExperimentContext, ParticipantSubmission, ParticipantSubmissionAnswer


class ExperimentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='_id', read_only=True)

    class Meta:
        model = Experiment
        fields = ['id', 'user', 'created_at', 'updated_at', 'name', 'description']


class ParticipantSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='_id', read_only=True)

    class Meta:
        model = Participant
        fields = ['id', 'created_at', 'participant_code']


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='_id', read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'created_at', 'updated_at', 'question_text', 'max_answers']


class QuestionAnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='_id', read_only=True)

    class Meta:
        model = QuestionAnswer
        fields = ['id', 'created_at', 'updated_at', 'question', 'answer_text']


class ContextSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='_id', read_only=True)

    class Meta:
        model = Context
        fields = ['id', 'created_at', 'updated_at', 'context_id', 'context_name', 'context_description']


class ContextQuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='_id', read_only=True)

    class Meta:
        model = ContextQuestion
        fields = ['id', 'created_at', 'updated_at', 'context_id', 'question_id']


class ExperimentContextSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='_id', read_only=True)

    class Meta:
        model = ExperimentContext
        fields = ['id', 'created_at', 'updated_at', 'experiment', 'context']


class ParticipantSubmissionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='_id', read_only=True)

    class Meta:
        model = ParticipantSubmission
        fields = ['id', 'created_at', 'updated_at', 'participant', 'experiment_context']


class ParticipantSubmissionAnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='_id', read_only=True)

    class Meta:
        model = ParticipantSubmissionAnswer
        fields = ['id', 'created_at', 'updated_at', 'participant_submission', 'question_answer']