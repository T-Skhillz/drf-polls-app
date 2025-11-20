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
        