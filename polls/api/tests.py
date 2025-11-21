from rest_framework.test import APITestCase
from ..models import Question
from django.contrib.auth.models import User
from django.urls import reverse

class QuestionAPITest(APITestCase):
    def setUp(self):
        self.user_owner = User.objects.create_user(username="owner", password="pass")
        self.user_intruder = User.objects.create_user(username="intruder", password="pass")

        self.question_owner = Question.objects.create(
            user = self.user_owner,
            title = "Owner question",
        )

        self.question_intruder = Question.objects.create(
            user = self.user_intruder,
            title = "Intruder question",
        )

        self.question_list_url = reverse("question-list")
        self.question_detail_url = reverse("question-detail", kwargs={"pk" : self.question_owner.id})
        self.data = {
            "title" : "Title for API Question.",
        }
        self.updated_data = {
            "title" : "Updated title for API Question."
        }

    def test_authenticated_user_can_see_their_question_list(self):
        self.client.force_authenticate(user = self.user_owner)
        response = self.client.get(self.question_list_url)
        self.assertEqual(response.status_code, 200)
        returned_ids = [question["id"] for question in response.data]
        expected_ids = [self.question_owner.id]
        self.assertCountEqual(expected_ids, returned_ids)

    def test_unauthenticated_user_cannot_see_question_list(self):
        self.client.force_authenticate(user = None)
        response = self.client.get(self.question_list_url)
        self.assertEqual(response.status_code, 403)

    def test_authenticated_user_cannot_see_another_user_question_details(self):
        self.client.force_authenticate(user = self.user_intruder)
        response = self.client.get(self.question_detail_url)
        self.assertEqual(response.status_code, 403)

    def test_authenticated_user_can_see_their_own_question_details(self):
        self.client.force_authenticate(user = self.user_owner)
        response = self.client.get(self.question_detail_url)
        self.assertEqual(response.status_code, 200)
        returned_id = [response.data["id"]]
        expected_id = [self.question_owner.id]
        self.assertEqual(expected_id, returned_id)

    def test_authenticated_user_can_create_question(self):
        self.client.force_authenticate(user = self.user_owner)
        initial_question_count = Question.objects.count()
        response = self.client.post(self.question_list_url, data=self.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Question.objects.count(), initial_question_count + 1)

    def test_unauthorized_user_cannot_create_question(self):
        self.client.force_authenticate(user = None)
        initial_question_count = Question.objects.count()
        response = self.client.post(self.question_list_url, data=self.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Question.objects.count(), initial_question_count)

    def test_authenticated_user_can_update_their_question(self):
        self.client.force_authenticate(user = self.user_owner)
        response = self.client.patch(self.question_detail_url, data=self.updated_data, format="json")
        self.assertEqual(response.status_code, 200)
        updated_question = Question.objects.get(id = self.question_owner.id)
        self.assertEqual(updated_question.title, self.updated_data["title"])

    def test_authenticated_user_cannot_update_another_user_question(self):
        self.client.force_authenticate(user = self.user_intruder)
        response = self.client.patch(self.question_detail_url, data=self.updated_data, format="json")
        self.assertEqual(response.status_code, 403)

    def test_unauthorized_user_cannot_update_question(self):
        self.client.force_authenticate(user = None)
        response = self.client.patch(self.question_detail_url, data=self.updated_data, format="json")
        self.assertEqual(response.status_code, 403)
