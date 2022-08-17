from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from apps.payroll.api.serializers import PayrollSerializer
from datetime import datetime
from datetime import date
from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer
from apps.employees.models import Employee
import coreapi
import calendar

class SimpleFilterBackend(DjangoFilterBackend): #Making schemas for Swagger
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
            name='month',
            location='query',
            required=True,
            type='datetime'),
            coreapi.Field(
            name='employee__company',
            location='query',
            required=True,
            type='integer'),
            coreapi.Field(
            name='employee_id',
            location='query',
            required=True,
            type='integer'),
        ]

@permission_classes([IsAuthenticated])
class PayrollViewSet (XLSXFileMixin,viewsets.ReadOnlyModelViewSet):

    serializer_class = PayrollSerializer
    filter_backends = [SimpleFilterBackend]
    filterset_fields = ['employee__company','employee_id']
    renderer_classes = (XLSXRenderer,)
    column_header = { #Styilizing the excel sheet
        'titles': [
                "Company",
                "Employee name",
                "Role",
                "Date",
                "Attendance",
                "Hours worked"
            ],
        'height': 25,
        'column_width': [20, 30, 20, 20, 20, 20],
        'style': {
            'fill': {
                'fill_type': 'solid',
                'start_color': '235E83',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': False,
                'shrink_to_fit': False,
            },
            'border_side': {
                'border_style': 'thick',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Century Gothic',
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
                'start_color': 'E9F6D2',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': False,
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Century Gothic',
                'size': 10,
                'bold': False,
                'color': 'FF000000',
            }
        },
        'height': 40,
    }
    
    def get_queryset(self, pk = None):
        date = self.get_dateFilter(self.request.GET.get('month')) # Getting the first day of the month required by the user

        if pk is None:
            if date:
                return self.get_serializer().Meta.model.objects.filter(date__range = (date['initial_date'], date['final_date']))
        return self.get_serializer().Meta.model.objects.filter(id = pk).first()

    def get_filename(self, request): # Defining the name of the file generated
        if self.request.GET.get('employee_id'):
            employee = Employee.objects.filter(id = self.request.GET.get('employee_id')).first()
            name = f"{employee.name}{employee.last_name}_payroll.xlsx"
        else:
            name = 'payroll.xlsx'
            
        return name   

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
