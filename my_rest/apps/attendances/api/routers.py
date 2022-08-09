from rest_framework.routers import DefaultRouter
from apps.attendances.api.api import AttendanceViewSet, AttendanceByEmployeeAPIView

router = DefaultRouter()

router.register(r'attendance', AttendanceViewSet, basename = 'attendance')

urlpatterns = router.urls