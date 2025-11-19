from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from ..serializers import QuestionSerializer
from ..models import Question

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user
    
class QuestionViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(user = self.request.user).order_by("-created_at")
    
    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)
