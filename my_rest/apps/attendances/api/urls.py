from django.urls import URLPattern, path
from apps.attendances.api.api import AttendanceByEmployeeAPIView

urlpatterns = [
    path('attendanceByEmployee/<int:id>/', AttendanceByEmployeeAPIView.as_view(), name = 'Users by id url')
]