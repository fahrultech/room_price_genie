# RoomPriceGenie Task No1

## Task Description
You will be asked to implement two modules: Data Provider and the Dashboard Service. You can use any
framework for both modules, however using FastAPI/Django/Flask is preferred. Below you can find the description
of the modules and the requirements for each of them.

## Stack
The Stack for this app
- Django Rest Framework
- Postgresql
- Celery
- Celery Beat
- Redis
- Docker
- Swagger

## Project End Goal
1. Some data has to be periodically added to the Data Provider’s database using POST /events endpoint - this
is basically a simulation of data coming from the hotel into the booking management system.
2. There needs to be a periodic task that fills in the Dashboard Service’s database using the Data Provider’s
GET /events endpoint. The data should be requested based on the event’s timestamp(please, reference the
request parameters).
3. We should be able to trigger the GET /dashboard endpoint through Swagger and get the necessary data.

## Usage

### Env Variables
Create .env file in the root and add the following

```
DEBUG=1
SECRET_KEY=4lspt&&o$l@3*j9wm@-6ou_+zf-d93wrklq7yx_97296^^gj&-
POSTGRES_DB=roompricegenie_db
POSTGRES_USER=genie
POSTGRES_PASSWORD=genie
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### Run the app
```
docker compose up --build
```

### Database
After running docker this app already include the command to insert data to database
```
#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate
python manage.py load_data_from_csv

# Start the server
echo "Starting the web server..."
exec "$@"
```

### Testing
For unit test use below command:
```
docker compose exec web pytest
```

### Access the api
#### Data Provider
- You access the data provider api through swagger 
```
http://localhost:8000/swagger/
```
- GET /events - returns a list of events happened within a particular hotel. The list should be sorted by the
timestamp in ascending order. The following query parameters should be supported:
```
http://localhost:8000/api/events?hotel_id=3539&updated__lte=2022-03-01&updated__gte=2022-02-20&rpg_status=1&night_of_stay__gte=2022-03-17&night_of_stay__lte=2022-04-30&room_id=264171101

query parameter : 
    "hotel_id":1
    "updated__lte":2022-03-01
    "updated__gte":2022-02-01
    "rpg_status":1
    "night_of_stay__gte": 2022-03-17
    "night_of_stay__lte": 2022-04-30
    "room_id": 26471101
```
- POST /events - creates a new event. The event should be validated according to the schema above. The
event should be saved to the database.
```
http://localhost:8000/api/events/
bodyParameter : 
{
    "hotel_id": 2456,
    "rpg_status": 1,
    "room_id": "433333",
    "night_of_stay": "2024-10-10"
}

```

#### Dashboard Service
- You can access dashboard service api through swagger

```
http://localhost:8000/swagger/
```
- GET /dashboard - returns the dashboard information for a particular hotel.
```
http://localhost:8080/api/dashboard?hotel_id=2607&period=month&year=2022
queryParameter :
    "hotel_id": 2607
    "period": "month" or "day"
    "year": 2022
```

#### End Goal
1. Some data has to be periodically added to the Data Provider’s database using POST /events endpoint - this
is basically a simulation of data coming from the hotel into the booking management system.
2. There needs to be a periodic task that fills in the Dashboard Service’s database using the Data Provider’s
GET /events endpoint. The data should be requested based on the event’s timestamp(please, reference the
request parameters).
3. We should be able to trigger the GET /dashboard endpoint through Swagger and get the necessary data.
Below are the parts of celery.py which is periodically send to Data Providers database and also get data from Data Provider database and send to Dashboard Service Database
```
app.conf.beat_schedule = {
    'add-event-every-five-minute': { # End Goal Task #1
        'task': 'data_provider.tasks.add_event_to_data_provider',
        'schedule': crontab(minute='*/5'),  # Runs every 5 minutes
    },
    'populate-dashboard-ten-minute': { # End Goal Task #2
        'task': 'dashboard.tasks.populate_dashboard_service',
        'schedule': crontab(minute='*/15'),  # Runs every 15 minutes 
    },
}
```

#### Requirements

As we can see in the unit test below the populate data to dashboard test already mock the events service response

```
@pytest.mark.django_db
@patch('dashboard.services.dashboard_service.requests.get')
def test_populate_dashboard(mock_get, dashboard_service, mock_repository):
    # Arrange
    mock_data_provider_response = [
        {'hotel_id': 1, 'timestamp': '2024-01-01T00:00:00Z', 'rpg_status': 1, 'night_of_stay': '2024-01-01'},
        {'hotel_id': 1, 'timestamp': '2024-01-01T00:05:00Z', 'rpg_status': 1, 'night_of_stay': '2024-01-01'}
    ]
    mock_get.return_value.json.return_value = mock_data_provider_response
    mock_get.return_value.status_code = 200

    # Mock last processed range
    last_processed_range = ProcessedDateRange(start_date=datetime(2020, 1, 1), end_date=datetime(2020, 1, 31,))
    ProcessedDateRange.objects.create(start_date=last_processed_range.start_date, end_date=last_processed_range.end_date)

    # Act
    dashboard_service.populate_dashboard()

    # Assert
    mock_get.assert_called_once()
    assert Dashboard.objects.count() == 2
    assert ProcessedDateRange.objects.count() == 2
```