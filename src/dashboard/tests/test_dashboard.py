import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from dashboard.services.dashboard_service import DashboardService
from dashboard.models import Dashboard, ProcessedDateRange
from dashboard.repositories.dashboard_repository import IDashboardRepository

@pytest.fixture
def mock_repository():
    return MagicMock(spec=IDashboardRepository)

@pytest.fixture
def dashboard_service(mock_repository):
    return DashboardService(repository=mock_repository)

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

@pytest.mark.django_db
def test_get_monthly_dashboard(dashboard_service, mock_repository):
    # Arrange
    mock_entry = Dashboard(hotel_id=1, year=2024, month=1, bookings_count=10)
    mock_repository.get_monthly_report.return_value = [mock_entry]

    # Act
    data = dashboard_service.get_monthly_dashboard(hotel_id=1, year=2024)

    # Assert
    expected_data = [{'hotel_id': 1, 'year': 2024, 'month': 1, 'day': None, 'bookings_count': 10}]
    assert data == expected_data
    mock_repository.get_monthly_report.assert_called_once_with(hotel_id=1, year=2024)

@pytest.mark.django_db
def test_get_daily_dashboard(dashboard_service, mock_repository):
    # Arrange
    mock_entry = Dashboard(hotel_id=1, year=2024, month=1, day=datetime(2024, 1, 1).date(), bookings_count=5)
    mock_repository.get_daily_report.return_value = [mock_entry]

    # Act
    data = dashboard_service.get_daily_dashboard(hotel_id=1, year=2024)

    # Assert
    #expected_data = [{'hotel_id': 1, 'year': 2024, 'month': 1, 'day': '2024-01-01', 'bookings_count': 5}]
    # expected_data = {
    # "hotel_id": "2607",
    # "year": "2022",
    # "period": "day",
    # "data": [
    #     {
    #         "hotel_id": 2607,
    #         "year": 2022,
    #         "month": 1,
    #         "day": "2022-01-29",
    #         "bookings_count": 21590
    #     },
    # ]
    # }
    expected_data = [
        {
            "hotel_id": 1,
            "year": 2024,
            "month": 1,
            "day": "2024-01-01",
            "bookings_count": 5
        }
    ]
    
    print("heree")
    assert data == expected_data
    print("there")
    mock_repository.get_daily_report.assert_called_once_with(hotel_id=1, year=2024)
