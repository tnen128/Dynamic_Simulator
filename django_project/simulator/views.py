from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Kpi

class KpiEndpoint(APIView):
    def post(self, request, *args, **kwargs):
        value = request.data.get("value")
        kpi_id = request.data.get("kpi_id")
        kpi = Kpi.objects.get(id=kpi_id)
        result = kpi.calculate(value)
        return Response({"result": result})
