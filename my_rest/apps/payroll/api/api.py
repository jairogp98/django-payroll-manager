from xml.etree.ElementTree import tostring
from rest_framework.views import Response, APIView
from apps.attendances.models import Attendance
from rest_framework import status, viewsets
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from apps.payroll.api.serializers import PayrollFilterSerializer, PayrollOutputSerializer
from datetime import datetime
from datetime import date
from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer
from apps.employees.models import Employee
from apps.companies.models import Company
import coreapi
import calendar

class SimpleFilterBackend(DjangoFilterBackend): #Making schemas for Swagger
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
            name='date',
            location='query',
            required=True,
            type='datetime'),
            coreapi.Field(
            name='employee__company',
            location='query',
            required=False,
            type='integer'),
            coreapi.Field(
            name='employee_id',
            location='query',
            required=False,
            type='integer'),
        ]

#@permission_classes([IsAuthenticated])
class PayrollViewSet (XLSXFileMixin,viewsets.ReadOnlyModelViewSet):
    serializer_class = PayrollOutputSerializer
    filter_backends = [SimpleFilterBackend]
    filterset_fields = ['employee__company','employee_id']
    renderer_classes = (XLSXRenderer,)
    column_header = {
        'titles': [
            "Su",
            "Puta",
            "Madre",
        ],
        'column_width': [17, 30, 17],
        'height': 25,
        'style': {
            'fill': {
                'fill_type': 'solid',
                'start_color': 'FFCCFFCC',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Arial',
                'size': 14,
                'bold': True,
                'color': 'FF000000',
            },
        },
    }
    body = {
        'style': {
            'fill': {
                'fill_type': 'solid',
                'start_color': 'FFCCFFCC',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Arial',
                'size': 14,
                'bold': False,
                'color': 'FF000000',
            }
        },
        'height': 40,
    }
    
    def get_filename(self, request): # Defining the name of the file generated
        if self.request.GET.get('employee_id'):
            employee = Employee.objects.filter(id = self.request.GET.get('employee_id')).first()
            name = f"{employee.name}{employee.last_name}_payroll.xlsx"
        elif self.request.GET.get('employee__company'):
            company = Company.objects.filter(id = self.request.GET.get('employee__company')).first()
            name = f"{company.name}_payroll.xlsx"
        else:
            name = 'payroll.xlsx'
            
        return name
    
    def get_queryset(self, pk = None):
        date = self.get_dateFilter(self.request.GET.get('date')) # Getting the first day of the month required by the user

        if pk is None:
            if date:
                return self.get_serializer().Meta.model.objects.filter(date__range = (date['initial_date'], date['final_date']))
        return self.get_serializer().Meta.model.objects.filter(id = pk).first()

    def get_dateFilter(self, month): # This funcion gets the range of dates that i need for the month filtering in the queryset ex: 2022-01-01, 2022-01-31
        initial_month = month
        if initial_month:
            initial_month = datetime.strptime(initial_month, '%Y-%m-%d %H:%M:%S.%f')
            year = initial_month.year
            month = initial_month.month
            day = initial_month.day
            range = calendar.monthrange(year,month)
            final_day = range[1]
            initial_date = date(year,month,day)
            final_date = date(year,month, final_day)

            return {"initial_date": initial_date, "final_date": final_date}
        
    """ def list(self, request):
        
        try:
            serialized_input = PayrollFilterSerializer(data = request.GET)
            if serialized_input.is_valid():
                serializer_output = self.get_serializer(self.filter_queryset(self.get_queryset()), many = True)
                excel = self.create_excel(serializer_output)
                return Response(excel.data,200)
            else:
                return Response(serialized_input.errors)
            
        except Exception as e:
                return Response (f"ERROR: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR) """

    def create_excel(self, data):
        return data
