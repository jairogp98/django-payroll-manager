from rest_framework.routers import DefaultRouter
from apps.payroll.api.api import PayrollViewSet

router = DefaultRouter()

router.register(r'payroll', PayrollViewSet, basename = 'payroll')

urlpatterns = router.urls