from django.test import TestCase
from django.test import Client

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from .models import *
from .django.contrib.auth import get_user_model
from serializers import *

User = get_user_model()


class ExperimentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            username='testuser',
            password='testpass')
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
        self.user = User.objects.create_user(
            email='test@test.com',
            username='testuser',
            password='testpass')
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
        self.user = User.objects.create_user(
            email='test@test.com',
            username='testuser',
            password='testpass')
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
        self.user = User.objects.create_user(
            email='test@test.com',
            username='testuser',
            password='testpass')
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


class ParticipantSubmissionTests(APITestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.participant = Participant.objects.create(
            participant_code='123456'
        )
        self.context = Context.objects.create(
            name='Test Context',
            description='This is a test context'
        )
        self.question = Question.objects.create(
            context=self.context,
            description='Test question'
        )
        self.answer = Answer.objects.create(
            text='Test answer',
            question=self.question
        )


class ParticipantSubmissionTests(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', email='admin@example.com', password='testpassword')
        self.participant = Participant.objects.create(participant_code='abc123')
        self.experiment = Experiment.objects.create(exp_admin=self.admin_user, name='Test Experiment',
                                                    description='This is a test experiment')
        self.context = Context.objects.create(name='Test Context', description='This is a test context',
                                              experiment=self.experiment)
        self.question = Question.objects.create(context=self.context, description='Test Question')
        self.answer = Answer.objects.create(text='Test Answer', question=self.question)

    def test_create_participant_submission(self):
        url = reverse('participant_submission')
        data = {
            'participant': 'abc123',
            'context': self.context.id,
            'question': self.question.id,
            'answer': self.answer.id
        }
        self.client.login(username='admin', password='testpassword')
        response = self.client.post(url, data, headers={"Content-type":"application/json"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        participant_submission = ParticipantSubmission.objects.get(id=response.data['id'])
        serializer = ParticipantSubmissionSerializer(participant_submission)
        self.assertEqual(response.data, serializer.data)

    def test_create_participant_submission_invalid_participant(self):
        url = reverse('participant_submission')
        data = {
            'participant': 'invalidparticipantcode',
            'context': self.context.id,
            'question': self.question.id,
            'answer': self.answer.id
        }
        self.client.login(username='admin', password='testpassword')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_create_participant_submission_missing_data(self):
        url = reverse('participant_submission')
        data = {
            'participant': 'abc123'
        }
        self.client.login(username='admin', password='testpassword')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

class SubmittionPostTestCase(APITestCase):

    def test_successful_submission(self):
        experiment = Experiment.objects.create(name='Experiment')
        participant = Participant.objects.create(participant_code='123')
        participant_experiment = ParticipantExperiment.objects.create(experiment=experiment, participant=participant)
        context = Context.objects.create(context_id='456')
        question = Question.objects.create(question_id='789')
        answer = Answer.objects.create(answer_id='abc')

        data = {
            'context_id': context.id,
            'participant': participant.participant_code,
            'experiment_id': experiment.id,
            'question_id': question.id,
            'answer_id': answer.id
        }

        response = self.client.post('/api/submission/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ParticipantSubmission.objects.count(), 1)

    def test_missing_data(self):
        response = self.client.post('/api/submission/', {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ParticipantSubmission.objects.count(), 0)

    def test_invalid_experiment(self):
        participant = Participant.objects.create(participant_code='123')
        context = Context.objects.create(context_id='456')
        question = Question.objects.create(question_id='789')
        answer = Answer.objects.create(answer_id='abc')

        data = {
            'context_id': context.id,
            'participant': participant.participant_code,
            'experiment_id': 999,  # Invalid experiment ID
            'question_id': question.id,
            'answer_id': answer.id
        }

        response = self.client.post('/api/submission/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ParticipantSubmission.objects.count(), 0)

    def test_invalid_participant(self):
        experiment = Experiment.objects.create(name='Experiment')
        context = Context.objects.create(context_id='456')
        question = Question.objects.create(question_id='789')
        answer = Answer.objects.create(answer_id='abc')

        data = {
            'context_id': context.id,
            'participant': 'invalid_participant_code',  # Invalid participant code
            'experiment_id': experiment.id,
            'question_id': question.id,
            'answer_id': answer.id
        }

        response = self.client.post('/api/submission/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ParticipantSubmission.objects.count(), 0)
