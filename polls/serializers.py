from rest_framework import serializers
from .models import Question, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["question", "choice_text", "votes"]

class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = "user.username")
    choices = ChoiceSerializer(many = True, read_only = True)

    class Meta:
        model = Question
        fields = ["title", "created_at", "choices", "user", "id"]