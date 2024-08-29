import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from data_provider.models import Event

class Command(BaseCommand):
    help = 'Load data from CSV into the database'

    def handle(self, *args, **kwargs):
        if Event.objects.exists():
            self.stdout.write(self.style.SUCCESS('Database already contains data. Skipping CSV load.'))
            return

        csv_file_path = settings.CSV_FILE_PATH
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            events = [
                Event(
                    room_id=row['room_reservation_id'],
                    hotel_id=row['hotel_id'],
                    timestamp=row['event_timestamp'],
                    rpg_status=row['status'],
                    id=row['id'],
                    night_of_stay=row['night_of_stay']
                )
                for row in reader
            ]

            Event.objects.bulk_create(events)
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(events)} events into the database.'))
