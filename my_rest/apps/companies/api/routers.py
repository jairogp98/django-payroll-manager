from rest_framework.routers import DefaultRouter
from apps.companies.api.api import CompanyViewSet

router = DefaultRouter()

router.register(r'company', CompanyViewSet, basename = 'company')

urlpatterns = router.urls