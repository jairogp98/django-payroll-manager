from rest_framework.views import Response
from apps.employees.api.serializers import EmployeeSerializer
from rest_framework import status, viewsets
from django.utils import timezone

class EmployeeViewSet(viewsets.ModelViewSet):

    serializer_class = EmployeeSerializer
    
    def get_queryset(self, pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(deleted_date = None)
        return self.get_serializer().Meta.model.objects.filter(id = pk, deleted_date = None).first()

    def destroy(self, request, pk = None):
        """Personalized delete method bc the default viewset destroys the entire data. This is logical delete"""
        try:
            employee = self.get_queryset(pk)
            if employee is not None:
                employee.deleted_date = timezone.now()
                employee.save()
                return Response(f'Employee {employee.email} succesfully deleted', status.HTTP_200_OK)
            else:
                return Response({"message": "Employee not found"}, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response (f"ERROR: {e}", 500)
