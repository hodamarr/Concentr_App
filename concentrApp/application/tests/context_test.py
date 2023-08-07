from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from accounts.models import User
from ..models import Experiment, Context
import json

class ContextCreateViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            username='testuser',
            password='testpass'
        )
        self.experiment = Experiment.objects.create(
            exp_admin=self.user,
            name='Sample Experiment',
            description='Sample Experiment Description'
        )
        self.token = Token.objects.create(user=self.user)

    def test_create_context(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/api/context/'
        data = {
            'experiment': self.experiment.name,
            'name': 'Sample Context',
            'description': 'Sample Context Description'
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Context.objects.count(), 1)
        context = Context.objects.first()
        self.assertEqual(context.name, 'Sample Context')
        self.assertEqual(context.description, 'Sample Context Description')
        self.assertEqual(context.experiment, self.experiment)
        self.assertEqual(response.data['data']['id'], context.id)
        self.assertEqual(response.data['data']['name'], context.name)
        self.assertEqual(response.data['data']['description'], context.description)

    def test_get_contexts(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/api/context/'
        self.client.defaults['experiment'] = self.experiment
        self.context = Context.objects.create(
            name='Sample Context',
            description='Sample Context Description',
            experiment=self.experiment)
        response = self.client.get(url, None, **{"HTTP_EXPERIMENT": self.experiment.name})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)
        data = response.data['data']
        self.assertEqual(data[0]['id'], self.context.id)
        self.assertEqual(data[0]['name'], 'Sample Context')
        self.assertEqual(data[0]['description'], 'Sample Context Description')

    def test_get_contexts_experiment_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/api/context/'
        invalid_experiment_name = 'Invalid Experiment'

        response = self.client.get(url, headers={
            'Content-Type': 'application/json',
            'experiment': invalid_experiment_name
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Experiment matching query does not exist.')
