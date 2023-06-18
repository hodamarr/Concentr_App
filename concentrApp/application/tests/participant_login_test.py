from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Participant, Experiment
from ..serializers import ParticipantSerializer
from django.urls import reverse


class ParticipantLoginViewTestCase(APITestCase):
    def setUp(self):
        self.participant_code = 'ABC123'
        self.experiment_id = 1
        self.experiment = Experiment.objects.create(
            exp_admin_id=1,
            name='Sample Experiment',
            description='Sample Experiment Description'
        )
        self.participant = Participant.objects.create(
            participant_code=self.participant_code,
            expo_token='EXPO_TOKEN'
        )

    def test_participant_login_success(self):
        url = reverse('participant_login')
        data = {
            'participant': self.participant_code,
            'experiment_id': self.experiment_id
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'ok')

    def test_participant_login_invalid_participant_code(self):
        url = reverse('participant_login')
        data = {
            'participant': 'INVALID_CODE',
            'experiment_id': self.experiment_id
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_participant_login_invalid_experiment_id(self):
        url = reverse('participant_login')
        data = {
            'participant': self.participant_code,
            'experiment_id': 999
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_participant_update_token(self):
        url = reverse('participant_login_update', kwargs={'pk': self.participant_code})
        data = {
            'token': 'NEW_TOKEN'
        }

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['expo_token'], 'NEW_TOKEN')

    def test_participant_update_token_invalid_participant_code(self):
        url = reverse('participant_login_update', kwargs={'pk': 'INVALID_CODE'})
        data = {
            'token': 'NEW_TOKEN'
        }

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_participant_get_score(self):
    #     url = reverse('participant_login')
    #     url +='?code='+self.participant_code
    #
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['data'], self.participant.score)
