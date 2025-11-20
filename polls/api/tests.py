from rest_framework.test import APITestCase
from ..models import Question
from django.contrib.auth.models import User
from django.urls import reverse

class QuestionAPITest(APITestCase):
    def setUp(self):
        self.user_owner = User.objects.create_superuser(username="owner", password="pass")
        self.user_intruder = User.objects.create_superuser(username="intruder", password="pass")

        self.question_owner = Question.objects.create(
            user = self.user_owner,
            title = "Owner question",
        )

        self.question_intruder = Question.objects.create(
            user = self.user_intruder,
            title = "Intruder question",
        )

        self.question_list_url = reverse("question-list")
        self.question_detail_url = reverse("question-detail", args=[self.question_owner.id])
        self.data = {
            "title" : "Title for API Question.",
        }
        self.updated_data = {
            "title" : "Updated title for API Question."
        }

    def test_authenticated_user_can_view_their_question_list(self):
        self.client.force_authenticate(user = self.user_owner)
        response = self.get(self.question_list_url)
        self.assertEqual(response.status_code, 200)
        