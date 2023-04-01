from rest_framework import routers
from .views import CourseViewSet

router = routers.SimpleRouter()
router.register(r"", CourseViewSet)

urlpatterns = router.urls
