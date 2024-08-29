from abc import ABC, abstractmethod
from typing import Dict
from datetime import datetime, timedelta
from collections import defaultdict
import requests
from dateutil import parser
from dashboard.models import Dashboard, ProcessedDateRange
from dashboard.api.serializers import DashboardSerializer
from dashboard.repositories.dashboard_repository import IDashboardRepository
import logging

class IDashboardService(ABC):
    @abstractmethod
    def populate_dashboard(self):
        pass

    @abstractmethod
    def get_monthly_dashboard(self, hotel_id: int, year: int) -> Dict[str, int]:
        pass

    @abstractmethod
    def get_daily_dashboard(self, hotel_id: int, year: int) -> Dict[str, int]:
        pass

class DashboardService(IDashboardService):
    def __init__(self, repository: IDashboardRepository):
        self.repository = repository
    
    def fetch_data_from_provider(self, start_datetime, end_datetime):
        response = requests.get('http://web:8000/api/events/', params={
            'updated__gte': f"{start_datetime.isoformat()}Z",
            'updated__lte': f"{end_datetime.isoformat()}Z",
        })
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve data from data provider: {response.status_code}")
        return response.json()
    
    def populate_dashboard(self):
        last_processed_range = ProcessedDateRange.objects.order_by('-end_date').first()

        if last_processed_range:
            next_start_datetime = last_processed_range.end_date + timedelta(seconds=1)
        else:
            next_start_datetime = datetime(2022, 1, 1, 0, 0)

        next_end_datetime = next_start_datetime + timedelta(minutes=5)

        # Check if this range has already been processed
        if ProcessedDateRange.objects.filter(start_date=next_start_datetime, end_date=next_end_datetime).exists():
            print(f"Skipping already processed range: {next_start_datetime} to {next_end_datetime}")
            return

        events = self.fetch_data_from_provider(next_start_datetime, next_end_datetime)
        
        aggregated_data = defaultdict(lambda: defaultdict(int))

        for event in events:
            event_date = parser.parse(event['timestamp'])
            year = event_date.year
            hotel_id = event['hotel_id']

            key_month = (hotel_id, year, event_date.month)
            key_day = (hotel_id, year, event_date.month, event_date.day)

            aggregated_data[key_month]['monthly'] += 1
            aggregated_data[key_day]['daily'] += 1
        
        for key, counts in aggregated_data.items():
            hotel_id, year, month = key[:3]
            if 'monthly' in counts:
                Dashboard.objects.update_or_create(
                    hotel_id=hotel_id,
                    year=year,
                    month=month,
                    defaults={'bookings_count': counts['monthly']}
                )
            if len(key) == 4 and 'daily' in counts:
                day = key[3]
                Dashboard.objects.update_or_create(
                    hotel_id=hotel_id,
                    year=year,
                    month=month,
                    day=datetime(year, month, day).date(),  # Convert datetime to date
                    defaults={'bookings_count': counts['daily']}
                )

        ProcessedDateRange.objects.create(start_date=next_start_datetime, end_date=next_end_datetime)

        print(f"Processed data for range: {next_start_datetime} to {next_end_datetime}")

    def get_monthly_dashboard(self, hotel_id: int, year: int):
        entries = self.repository.get_monthly_report(hotel_id=hotel_id, year=year)
        serializer = DashboardSerializer(entries, many=True)
        return serializer.data

    def get_daily_dashboard(self, hotel_id: int, year: int):
        entries = self.repository.get_daily_report(hotel_id=hotel_id, year=year)
        serializer = DashboardSerializer(entries, many=True)
        return serializer.data
