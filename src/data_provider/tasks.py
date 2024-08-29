from celery import shared_task
import uuid
from django.utils import timezone
import requests

@shared_task
def add_event_to_data_provider():
    data = {
        'room_id': str(uuid.uuid4()),
        'hotel_id': 123,
        'timestamp': timezone.now().isoformat(),
        'rpg_status': 1,
        'night_of_stay': timezone.now().date().isoformat(),
    }
    response = requests.post('http://web:8000/api/events/', json=data)
    return response.json()