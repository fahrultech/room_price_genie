from rest_framework import status, viewsets
from rest_framework.response import Response
from dashboard.api.serializers import DashboardSerializer
from dashboard.services.dashboard_service import DashboardService
from dashboard.repositories.dashboard_repository import DashboardRepository
from dashboard.models import Dashboard
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi

class DashboardViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dashboard_service = DashboardService(DashboardRepository())
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('hotel_id', openapi.IN_QUERY, description="ID of the hotel", type=openapi.TYPE_INTEGER),
            openapi.Parameter('period', openapi.IN_QUERY, description="Period of Dashboard( month or day )", type=openapi.TYPE_STRING),
            openapi.Parameter('year', openapi.IN_QUERY, description="Year of the dashboard", type=openapi.TYPE_STRING),
        ]
    )

    def list(self, request):
        hotel_id = request.GET.get('hotel_id')
        year = request.GET.get('year')
        period = request.GET.get('period')  # 'month' or 'day'

        if not hotel_id or not year or not period:
            return Response({"error": "Missing required parameters."}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize the repository and service
        repository = DashboardRepository()
        service = DashboardService(repository)

        if period == 'month':
            data = service.get_monthly_dashboard(hotel_id=int(hotel_id), year=int(year))
        elif period == 'day':
            data = service.get_daily_dashboard(hotel_id=int(hotel_id), year=int(year))
        else:
            return Response({"error": "Invalid period parameter."}, status=status.HTTP_400_BAD_REQUEST)

        # Convert the aggregated data into a list of DashboardEntry instances
        return Response({
            "hotel_id": hotel_id,
            "year": year,
            "period": period,
            "data": data  # This is now a dictionary, so no need to call .items()
        })