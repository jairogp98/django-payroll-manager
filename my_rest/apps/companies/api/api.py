from rest_framework.views import Response
from apps.companies.api.serializers import CompanySerializer
from rest_framework import status, viewsets
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

@permission_classes([IsAuthenticated])
class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer

    def get_queryset(self, pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(deleted_date = None)
        return self.get_serializer().Meta.model.objects.filter(id = pk, deleted_date = None).first()

    def destroy(self, request, pk = None):
        """Personalized delete method bc the default viewset destroys the entire data. This is logical delete"""
        try:
            company = self.get_queryset(pk)
            if company is not None:
                company.deleted_date = timezone.now()
                company.save()
                return Response(f'Company {company.name} succesfully deleted', status.HTTP_200_OK)
            else:
                return Response({"message": "Company not found"}, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response (f"ERROR: {e}", 500)