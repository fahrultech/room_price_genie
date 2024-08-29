from celery import shared_task
import requests
from datetime import datetime, timedelta
from collections import defaultdict
from dashboard.models import Dashboard, ProcessedDateRange
from dateutil import parser

@shared_task
def populate_dashboard_service():
    """
    Periodically populates the dashboard with aggregated booking data from the data provider.
    This task is based on the event's timestamp and processes data in 1-month increments.
    """
    # Determine the next date range to process
    last_processed_range = ProcessedDateRange.objects.order_by('-end_date').first()

    if last_processed_range:
        next_start_date = last_processed_range.end_date + timedelta(days=1)
    else:
        # If no data has been processed yet, start from a fixed date, e.g., January 1, 2022
        next_start_date = datetime(2022, 1, 1).date()

    # Calculate the end date for the next month
    next_end_date = (next_start_date.replace(day=1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    # Convert dates to ISO 8601 format for the API request
    start_datetime = f"{next_start_date.isoformat()}T00:00:00Z"
    end_datetime = f"{next_end_date.isoformat()}T23:59:59Z"

    # Fetch data from the data provider
    response = requests.get('http://web:8000/api/events/', params={
        'updated__gte': start_datetime,
        'updated__lte': end_datetime,
    })

    if response.status_code != 200:
        raise Exception(f"Failed to retrieve data from data provider: {response.status_code}")

    events = response.json()

    # Initialize a dictionary to store aggregated data
    # Initialize a dictionary to store aggregated data
    aggregated_data_month = defaultdict(int)
    aggregated_data_day = defaultdict(int)

    # Aggregate the data by hotel and day
    for event in events:
        event_date = event_date = parser.parse(event['timestamp'])
        year = event_date.year
        hotel_id = event['hotel_id']

        key_month = (hotel_id, year, event_date.month)
        key_day = (hotel_id, year, event_date.month, event_date.day)

        aggregated_data_month[key_month] += 1  # Monthly aggregation
        aggregated_data_day[key_day] += 1    # Daily aggregation

    # Store aggregated data in the DashboardEntry model
    # Store aggregated data in the DashboardEntry model
    for key, count in aggregated_data_month.items():
        hotel_id, year, month = key
        Dashboard.objects.update_or_create(
            hotel_id=hotel_id,
            year=year,
            month=month,
            defaults={'bookings_count': count}
        )

    for key, count in aggregated_data_day.items():
        hotel_id, year, month, day = key
        Dashboard.objects.update_or_create(
            hotel_id=hotel_id,
            year=year,
            month=month,
            day=datetime(year, month, day),
            defaults={'bookings_count': count}
        )
    # Mark this date range as processed
    ProcessedDateRange.objects.create(start_date=next_start_date, end_date=next_end_date)

    print(f"Processed data for range: {next_start_date} to {next_end_date}")
