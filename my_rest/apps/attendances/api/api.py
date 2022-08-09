from rest_framework.views import Response, APIView
from apps.attendances.api.serializers import AttendanceSerializer, AttendanceUpdateSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from drf_yasg.utils import swagger_auto_schema
from apps.attendances.models import Attendance
from django.utils import timezone

@permission_classes([IsAuthenticated])
class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    
    def get_queryset(self, pk = None):
        company = self.request.user.company # I need to filter by the company of the user logged in, so the user is not able to access another company's data.
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(employee__company= company)
        return self.get_serializer().Meta.model.objects.filter(id = pk, employee__company= company).first() # Getting pk as employee_id

    def create(self, request):

        #Checking if the employee has an open attendance first
        try:
            query = self.get_serializer().Meta.model.objects.filter(employee_id = request.data['employee'], exit_time__isnull = True).first()
            if not query:
                attendance_serialized = self.get_serializer(data =request.data)

                if attendance_serialized.is_valid():
                    attendance_serialized.save()
                    return Response(attendance_serialized.data, status.HTTP_201_CREATED)
                else:
                    return Response(attendance_serialized.errors)
                
            else:
                return Response({"message": f"This employee has an open attendance at {query.entrance_time}"}, status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response (f"ERROR: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes([IsAuthenticated])
class AttendanceByEmployeeAPIView(APIView):

    @swagger_auto_schema(responses={200: AttendanceSerializer(many=True)})
    def get(self,request, id:int):
        """Getting employee's attendances"""
        try:
            company = request.user.company
            if id is None:
                return Response({"message": "You must specify employee's id"}, status.HTTP_400_BAD_REQUEST)
            else:
                attendances = Attendance.objects.filter(employee_id = id, employee__company= company).all()
                if attendances is None:
                    return Response({"message": "No attendances found for this employee"}, status.HTTP_404_NOT_FOUND)
                else:
                    attendances_serialized = AttendanceSerializer(attendances, many = True)
                    return Response(attendances_serialized.data, status.HTTP_200_OK)
        except Exception as e:
                return Response (f"ERROR: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)


    @swagger_auto_schema(responses={200: AttendanceSerializer(many=True)}, request_body=AttendanceUpdateSerializer)
    def put (self, request, id:int):
        """Closing employee's attendance"""
        try:
            company = request.user.company
            if id is None:
                return Response({"message": "You must specify employee's id"}, status.HTTP_400_BAD_REQUEST)
            else:
                attendance = Attendance.objects.filter(employee_id = id, employee__company= company, date = request.data['date'], exit_time__isnull = True).first()
                if attendance is None:
                    return Response({"message": "No attendances found for this employee"}, status.HTTP_404_NOT_FOUND)
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
                        return Response(attendance_serialized.errors)
        except Exception as e:
            return Response (f"ERROR: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)        