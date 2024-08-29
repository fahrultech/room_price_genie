from rest_framework import status, viewsets
from rest_framework.response import Response
from data_provider.models import Event
from data_provider.api.serializers import EventSerializer
from data_provider.services.event_service import EventService
from data_provider.repositories.event_repository import EventRepository
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi

class EventViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event_service = EventService(EventRepository())
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('hotel_id', openapi.IN_QUERY, description="ID of the hotel", type=openapi.TYPE_INTEGER),
            openapi.Parameter('updated__gte', openapi.IN_QUERY, description="Start date of the event", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('updated__lte', openapi.IN_QUERY, description="End date of the event", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('rpg_status', openapi.IN_QUERY, description="Status of the event", type=openapi.TYPE_INTEGER),
            openapi.Parameter('room_id', openapi.IN_QUERY, description="ID of the room", type=openapi.TYPE_INTEGER),
            openapi.Parameter('night_of_stay__gte', openapi.IN_QUERY, description="Start date of stay", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('night_of_stay__lte', openapi.IN_QUERY, description="End date of stay", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
        ]
    )

    def list(self, request):
        filters = request.query_params.dict()
        events = self.event_service.list_events(filters)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            event_data = serializer.validated_data
            event = self.event_service.create_event(event_data)
            return Response(EventSerializer(event).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
