from django.urls import URLPattern, path
from apps.users.api.api import UserAPIView, UserAPIViewById 

urlpatterns = [
    path('user/', UserAPIView.as_view(), name = 'Users url'),
    path('user/<int:pk>/', UserAPIViewById.as_view(), name = 'Users by id url')
]