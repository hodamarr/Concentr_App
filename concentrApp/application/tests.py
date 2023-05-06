from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Experiment, Participant, ParticipantExperiment, Context, Question, Answer
from django.contrib.auth import get_user_model

User = get_user_model()

class ExperimentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@test.com' ,username='testuser', password='testpass')
        self.experiment = Experiment.objects.create(
            exp_admin=self.user,
            name='Test Experiment',
            description='This is a test experiment'
        )

    def test_experiment_creation(self):
        experiment = Experiment.objects.get(name='Test Experiment')
        self.assertEqual(experiment.exp_admin, self.user)
        self.assertEqual(experiment.description, 'This is a test experiment')

class ParticipantTestCase(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(
            participant_code='ABCDE'
        )

    def test_participant_creation(self):
        participant = Participant.objects.get(participant_code='ABCDE')
        self.assertEqual(participant.participant_code, 'ABCDE')

class ContextTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@test.com', username='testuser', password='testpass')
        self.experiment = Experiment.objects.create(
            exp_admin=self.user,
            name='Test Experiment',
            description='This is a test experiment'
        )
        self.context = Context.objects.create(
            name='Test Context',
            description='This is a test context',
            experiment=self.experiment
        )

    def test_context_creation(self):
        context = Context.objects.get(name='Test Context')
        self.assertEqual(context.name, 'Test Context')
        self.assertEqual(context.experiment, self.experiment)

class QuestionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@test.com' ,username='testuser', password='testpass')
        self.experiment = Experiment.objects.create(
            exp_admin=self.user,
            name='Test Experiment',
            description='This is a test experiment'
        )
        self.context = Context.objects.create(
            name='Test Context',
            description='This is a test context',
            experiment=self.experiment
        )
        self.question = Question.objects.create(
            description='This is a test question',
            context=self.context
        )

    def test_question_creation(self):
        question = Question.objects.get(description='This is a test question')
        self.assertEqual(question.context, self.context)
        self.assertEqual(question.description, 'This is a test question')

class AnswerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@test.com' ,username='testuser', password='testpass')
        self.experiment = Experiment.objects.create(
            exp_admin=self.user,
            name='Test Experiment',
            description='This is a test experiment'
        )
        self.context = Context.objects.create(
            name='Test Context',
            description='This is a test context',
            experiment=self.experiment
        )
        self.question = Question.objects.create(
            description='This is a test question',
            context=self.context
        )
        self.answer = Answer.objects.create(
            text='This is a test answer',
            question=self.question
        )

    def test_answer_creation(self):
        answer = Answer.objects.get(text='This is a test answer')
        self.assertEqual(answer.question, self.question)
        self.assertEqual(answer.text, 'This is a test answer')
