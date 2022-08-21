from rest_framework.views import Response, APIView
from apps.attendances.api.serializers import AttendanceSerializer, AttendanceUpdateSerializer, AttendanceCreateSerializer
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from drf_yasg.utils import swagger_auto_schema
from apps.attendances.models import Attendance
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
import coreapi

class SimpleFilterBackend(DjangoFilterBackend): #Making schemas for Swagger
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
            name='date',
            location='query',
            required=False,
            type='string'),
            coreapi.Field(
            name='employee_id',
            location='query',
            required=False,
            type='integer'),
            coreapi.Field(
            name='employee__company',
            location='query',
            required=True,
            type='integer'),
        ] 
        
@permission_classes([IsAuthenticated])
class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    filter_backends = [SimpleFilterBackend]
    filterset_fields = ['date','employee_id', 'employee__company']

    def get_queryset(self, pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        return self.get_serializer().Meta.model.objects.filter(id = pk).first()

    @swagger_auto_schema(responses={200: AttendanceSerializer(many=True)}, request_body=AttendanceCreateSerializer)
    def create(self, request):
        """Creating attendance"""
        try:
            query = self.get_serializer().Meta.model.objects.filter(employee_id = request.data['employee'], exit_time__isnull = True).first()
            if not query: #Checking if the employee has an open attendance first
                attendance_serialized = AttendanceCreateSerializer(data =request.data)
                if attendance_serialized.is_valid():
                    attendance_serialized.save()
                    return Response(attendance_serialized.data, status.HTTP_201_CREATED)
                else:
                    return Response(attendance_serialized.errors, status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response({"message": f"This employee has an open attendance at {query.entrance_time}"}, status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response (f"ERROR: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(responses={200: AttendanceSerializer(many=True)}, request_body=AttendanceUpdateSerializer)
    def update(self, request, pk):
        """Closing employee's attendance"""
        try:
            if pk is None:
                return Response({"message": "You must specify attendance's id"}, status.HTTP_400_BAD_REQUEST)
            else:
                attendance = self.get_serializer().Meta.model.objects.filter(id = pk, exit_time__isnull = True).first()
                if attendance is None:
                    return Response({"message": "The attendance is already closed or doesn't exist"}, status.HTTP_404_NOT_FOUND)
                else:
                    attendance_serialized = AttendanceUpdateSerializer(attendance, data = request.data)
                    if attendance_serialized.is_valid():
                        attendance.exit_time = timezone.now()
                        hours_worked = attendance.exit_time-attendance.entrance_time
                        hours_worked = round(hours_worked.seconds/3600, 2)
                        attendance.hours_worked = hours_worked
                        attendance_serialized.save()

                        #Returning the updated object
                        attendance_updated = AttendanceSerializer(attendance)
                        return Response(attendance_updated.data, status.HTTP_200_OK)
                    else:
                        return Response(attendance_serialized.errors, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response (f"ERROR: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk):
        return Response("message: This method is not currently in use", status.HTTP_200_OK)