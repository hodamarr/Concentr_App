from django.db import models  # noqa
from concentrApp import settings as stngs
import random as r
import string

"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


def __generate_code(k):
    """return 5 digit code"""
    return ''.join(r.choices(string.ascii_letters + string.digits, k=k))




class UserManager(BaseUserManager):
    """Manager for users."""
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Experiment(models.Model):
    user = models.ForeignKey(
        stngs.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField()



class Participant(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    participant_code = models.CharField(max_length=255, unique=True)


class Question(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    question_text = models.TextField()
    max_answers = models.IntegerField(default=5)


class QuestionAnswer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()


class Context(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    context_name = models.CharField(max_length=255)
    context_description = models.TextField(null=True, blank=True)


class ContextQuestion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    context_id = models.ForeignKey(Context, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('context_id', 'question_id')


class ExperimentContext(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    context = models.ForeignKey(Context, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('experiment_id', 'context_id')


class ParticipantSubmission(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    experiment_context = models.ForeignKey(ExperimentContext, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('participant_id', 'experiment_context_id')


class ParticipantSubmissionAnswer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    participant_submission = models.ForeignKey(ParticipantSubmission, on_delete=models.CASCADE)
    question_answer_id = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE)

