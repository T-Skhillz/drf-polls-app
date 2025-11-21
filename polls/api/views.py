from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from ..serializers import QuestionSerializer
from ..models import Question

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user
    
class QuestionViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer

    def get_object(self):
        obj = Question.objects.get(pk = self.kwargs["pk"])
        if obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to access this object!")
        return obj

    def get_queryset(self):
        return Question.objects.filter(user = self.request.user).order_by("-created_at")
    
    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)
