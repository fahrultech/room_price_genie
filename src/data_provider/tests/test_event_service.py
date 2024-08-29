import os
import pytest
from django.utils.timezone import now
from data_provider.services.event_service import EventService
from data_provider.repositories.event_repository import EventRepository
from data_provider.models import Event


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.roompricegenie.settings')

@pytest.fixture
def event_repository():
    return EventRepository()

@pytest.fixture
def event_service(event_repository):
    return EventService(event_repository)

@pytest.mark.django_db
def test_create_event(event_service):
    event_data = {
        "hotel_id": 1,
        "timestamp": now(),
        "rpg_status": Event.BOOKING,
        "room_id": 101,
        "night_of_stay": now().date()
    }
    event = event_service.create_event(event_data)
    assert event.id is not None

@pytest.mark.django_db
def test_list_events(event_service, event_repository):
    Event.objects.create(
        hotel_id=1, 
        timestamp=now(), 
        rpg_status=Event.BOOKING, 
        room_id=101, 
        night_of_stay=now().date()
    )
    filters = {"hotel_id": 1}
    events = event_service.list_events(filters)
    assert len(events) == 1