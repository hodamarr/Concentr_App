from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Participant(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    participant_code = models.CharField(max_length=255, unique=True)


class Experiment(models.Model):
    exp_admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="experiments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField()


class ParticipantExperiment(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Context(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    experiment = models.ForeignKey(
        Experiment,
        on_delete=models.CASCADE,
        related_name="contexts"
    )


class Question(models.Model):
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255)


class Answer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")




