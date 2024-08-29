from abc import ABC, abstractmethod
from typing import List, Dict
from dashboard.models import Dashboard

class IDashboardRepository(ABC):
    @abstractmethod
    def get_monthly_report(self, hotel_id: int, year: int) -> List[Dashboard]:
        pass

    @abstractmethod
    def get_daily_report(self, hotel_id: int, year: int) -> List[Dashboard]:
        pass

    @abstractmethod
    def save_entries(self, entries: List[Dashboard]) -> None:
        pass

class DashboardRepository(IDashboardRepository):
    def get_monthly_report(self, hotel_id: int, year: int) -> List[Dashboard]:
        return Dashboard.objects.filter(hotel_id=hotel_id, year=year, day__isnull=True)

    def get_daily_report(self, hotel_id: int, year: int) -> List[Dashboard]:
        return Dashboard.objects.filter(hotel_id=hotel_id, year=year, day__isnull=False)

    def save_entries(self, entries: List[Dashboard]) -> None:
        for entry in entries:
            entry.save()
