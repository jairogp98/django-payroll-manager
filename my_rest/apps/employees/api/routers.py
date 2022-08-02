from rest_framework.routers import DefaultRouter
from apps.employees.api.api import EmployeeViewSet

router = DefaultRouter()

router.register(r'employee', EmployeeViewSet, basename = 'employee')

urlpatterns = router.urls