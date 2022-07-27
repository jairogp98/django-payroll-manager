from rest_framework.views import APIView, Response
from apps.employees.models import Employee
from apps.employees.api.serializers import EmployeeCreateSerializer, EmployeeListSerializer, EmployeeUpdateSerializer
from rest_framework import status

class EmployeeAPIView(APIView):

    def get(self, request):
        try:
            employees = Employee.objects.filter(deleted_date = None)
            employees_serialized = EmployeeListSerializer(employees, many = True)
            return Response(employees_serialized.data, status.HTTP_200_OK)
        except Exception as e:
                return Response (f"ERROR: {e}", 500)        

    def post(self, request):
        try:
            serializer = EmployeeCreateSerializer(data = request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        except Exception as e:
                return Response (f"ERROR: {e}", 500)

class EmployeeByIdAPIView(APIView):

    def get(self, request, pk):
        try:
            if pk is None:
                return Response({"message": "You must specify Employee id"}, status.HTTP_400_BAD_REQUEST)
            else:
                employee = Employee.objects.filter(deleted_date = None).filter(id=pk).first()
                if employee is None:
                    return Response({"message": "Employee not found"}, status.HTTP_404_NOT_FOUND)
                else:
                    employee_serialized = EmployeeListSerializer(employee)
                    return Response(employee_serialized.data, status.HTTP_200_OK)
        except Exception as e:
                return Response (f"ERROR: {e}", 500)     

    def put(self, request, pk):
        try:
            if pk is None:
                return Response({"message": "You must specify Employee id"}, status.HTTP_400_BAD_REQUEST)
            else:
                employee = Employee.objects.filter(id = pk).first()
                if employee is None:
                    return Response({"message": "Employee not found"}, status.HTTP_404_NOT_FOUND)
                else:
                    employee_serialized = EmployeeUpdateSerializer(employee, data = request.data)
                    if employee_serialized.is_valid():
                        employee_serialized.save()
                        return Response(employee_serialized.data, status.HTTP_200_OK)
                    else:
                        return Response(employee_serialized.errors)
        except Exception as e:
            return Response (f"ERROR: {e}", 500)