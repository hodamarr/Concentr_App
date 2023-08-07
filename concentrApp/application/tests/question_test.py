from django.core.exceptions import ValidationError
from django.test import TestCase
from application.models import Experiment, Context, Question
from django.contrib.auth import get_user_model

User = get_user_model()


class TestQuestionModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', email='test@test.com', password='password')
        self.client.force_login(self.user)
        self.experiment = Experiment.objects.create(name="Test Experiment", description="Test Description",  exp_admin=self.user)
        self.context = Context.objects.create(name="Test Context", description="Test Description",
                                              experiment=self.experiment)

    def test_question_creation(self):
        parent_question = Question.objects.create(context=self.context, description="Parent Question")
        child_question = Question.objects.create(context=self.context, description="Child Question",
                                                 parent=parent_question)

        self.assertEqual(str(parent_question.description), "Parent Question")
        self.assertEqual(str(child_question.description), "Child Question")

        self.assertIsNone(parent_question.parent)
        self.assertEqual(child_question.parent, parent_question)

    def test_infinite_loop_validation(self):
        parent_question = Question.objects.create(context=self.context, description="Parent Question")
        child_question = Question.objects.create(context=self.context, description="Child Question",
                                                 parent=parent_question)

        with self.assertRaises(Exception) as context:
            parent_question.parent = child_question
            parent_question.save()

        self.assertEqual(str(context.exception), "['Infinite loop detected in nested questions.']")

        parent_question.refresh_from_db()
        self.assertIsNone(parent_question.parent)  # Ensure parent question was not changed

    def test_related_answer_default(self):
        question = Question.objects.create(context=self.context, description="Test Question")
        self.assertEqual(question.related_answer, -1)

    def test_related_answer_update(self):
        question = Question.objects.create(context=self.context, description="Test Question")
        question.related_answer = 42
        question.save()
        updated_question = Question.objects.get(id=question.id)
        self.assertEqual(updated_question.related_answer, 42)

    def test_str_representation(self):
        question = Question.objects.create(context=self.context, description="Test Question")
        self.assertEqual(str(question), f"{question.id}, Test Question")

    def test_save_valid_parent_cycle(self):
        question1 = Question.objects.create(context=self.context, description="Question 1")
        question2 = Question.objects.create(context=self.context, description="Question 2", parent=question1)

        question2.parent = question1
        question2.save()

        self.assertEqual(question2.parent, question1)