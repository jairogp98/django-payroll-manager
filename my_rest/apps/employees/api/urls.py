from django.urls import URLPattern, path
from apps.employees.api.api import EmployeeAPIView, EmployeeByIdAPIView

urlpatterns = [
    path('employees/', EmployeeAPIView.as_view(), name = 'Employees URL'),
    path('employees/<int:pk>/', EmployeeByIdAPIView.as_view(), name = 'Employee by id url')
]