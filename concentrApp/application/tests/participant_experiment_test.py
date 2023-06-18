from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from rest_framework.authtoken.models import Token
from ..models import Experiment, ParticipantExperiment, Participant
from ..serializers import ParticipantExperimentSerializer, ExperimentSerializer


class ParticipantExperimentCreateViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            username='testuser',
            password='testpass'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)  # Set authentication token in the request headers
        self.url = '/api/participants/'
        self.experiment = Experiment.objects.create(
            exp_admin=self.user,
            name='Sample Experiment',
            description='Sample Experiment Description'
        )

    def test_create_participant_experiment(self):
        data = {
            'experiment_id': self.experiment.name
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ParticipantExperiment.objects.count(), 1)
        participant_experiment = ParticipantExperiment.objects.first()
        self.assertEqual(participant_experiment.experiment, self.experiment)

    def test_get_experiment_participants(self):
        participant = Participant.objects.create(
            participant_code='ABC123',
            expo_token='EXPO_TOKEN'
        )
        participant_experiment = ParticipantExperiment.objects.create(
            participant=participant,
            experiment=self.experiment
        )

        response = self.client.get(self.url, {'experiment': self.experiment.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        participants = response.data
        self.assertEqual(len(participants['data']), 1)
        self.assertEqual(participants['data'][0]['code'], participant.participant_code)
        self.assertEqual(participants['data'][0]['score'], participant.score)
