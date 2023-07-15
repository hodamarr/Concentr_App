from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Participant(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    participant_code = models.CharField(max_length=255, unique=True)
    score = models.IntegerField(default=0)
    expo_token = models.TextField(null=True)
    is_female = models.BooleanField(default=True)



class Experiment(models.Model):
    exp_admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="experiments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, unique=True)
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
    parent_id = models.IntegerField(default=-1)


class Question(models.Model):
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    related_answer = models.IntegerField(default=-1)

    def __str__(self):
        return str(self.id) + ", " + self.description

    def validate_no_infinite_loop(self):
        parent = self.parent
        while parent is not None:
            if parent == self:
                raise ValidationError('Infinite loop detected in nested questions.')
            parent = parent.parent

    def save(self, *args, **kwargs):
        try:
            self.validate_no_infinite_loop()
            super().save(*args, **kwargs)
        except Exception as e:
            raise e


class Answer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.TextField()
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers")


class ParticipantSubmission(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, default=-1)

    class Meta:
        unique_together = ('participant', 'context', 'question')


class Schedule(models.Model):
    """
    {
        'time': '14:40',
    }
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    ping_times = models.TextField()
    context = models.ForeignKey(Context, on_delete=models.CASCADE, default=-1)
