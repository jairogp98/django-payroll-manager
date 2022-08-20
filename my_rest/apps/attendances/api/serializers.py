from rest_framework import serializers
from apps.attendances.models import Attendance

class AttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        exclude = ('exit_time',)
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class AttendanceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['date']

