from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from ..models import Experiment
from ..serializers import ExperimentSerializer
from rest_framework.authtoken.models import Token


class ExperimentListCreateViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            username='testuser',
            password='testpass'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)  # Set authentication token in the request headers
        self.url = '/api/experiments/'
        self.experiment_data = {
            'name': 'Sample Experiment',
            'description': 'Sample Experiment Description'
        }

    def test_create_experiment(self):
        response = self.client.post(self.url, self.experiment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Experiment.objects.count(), 1)
        experiment = Experiment.objects.first()
        self.assertEqual(experiment.name, self.experiment_data['name'])
        self.assertEqual(experiment.description, self.experiment_data['description'])

    def test_update_experiment(self):
        experiment = Experiment.objects.create(
            exp_admin=self.user,
            name='Sample Experiment',
            description='Sample Experiment Description'
        )
        update_data = {
            'name': 'Updated Experiment',
            'description': 'Updated Experiment Description'
        }

        response = self.client.patch(f'{self.url}{experiment.id}/', update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        experiment.refresh_from_db()
        self.assertEqual(experiment.name, update_data['name'])
        self.assertEqual(experiment.description, update_data['description'])

    def test_delete_experiment(self):
        experiment = Experiment.objects.create(
            exp_admin=self.user,
            name='Sample Experiment',
            description='Sample Experiment Description'
        )

        response = self.client.delete(f'{self.url}{experiment.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Experiment.objects.count(), 0)
