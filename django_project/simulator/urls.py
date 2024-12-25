from django.urls import path
from .views import KpiEndpoint

urlpatterns = [
    path('kpi/', KpiEndpoint.as_view(), name='kpi-endpoint'),
]
