from rest_framework import status
from ..models import Question, Answer, Experiment, Context
from accounts.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class AnswerCreateListViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            username='testuser',
            password='testpass'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.experiment = Experiment.objects.create(
            exp_admin=self.user,
            name='Sample Experiment',
            description='Sample Experiment Description'
        )
        self.context = Context.objects.create(
            name='Sample Context',
            description='Sample Context Description',
            experiment=self.experiment
        )
        self.question = Question.objects.create(
            context=self.context,
            description='Sample Question Description'
        )

    def test_create_answer(self):
        url = '/api/answer/'
        data = {
            'question_id': self.question.id,
            'text': 'Sample Answer Text'
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Answer.objects.count(), 1)
        answer = Answer.objects.first()
        self.assertEqual(answer.text, 'Sample Answer Text')
        self.assertEqual(answer.question, self.question)

    def test_get_answers(self):
        url = '/api/answer/?question_id={}'.format(self.question.id)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 0)

        answer = Answer.objects.create(
            question=self.question,
            text='Sample Answer Text'
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data['data'][0]['text'], 'Sample Answer Text')

    def test_delete_answer(self):
        answer = Answer.objects.create(
            question=self.question,
            text='Sample Answer Text'
        )
        url = '/api/answer/{}/'.format(answer.id)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Answer.objects.count(), 0)

    def test_update_answer(self):
        answer = Answer.objects.create(
            question=self.question,
            text='Sample Answer Text'
        )
        url = '/api/answer/{}/'.format(answer.id)
        data = {'text': 'Updated Answer Text'}

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        answer.refresh_from_db()
        self.assertEqual(answer.text, 'Updated Answer Text')