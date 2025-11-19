from rest_framework.routers import DefaultRouter
from .views import QuestionViewset

router = DefaultRouter()
router.register(r"questions", QuestionViewset, basename="question")
urlpatterns = router.urls