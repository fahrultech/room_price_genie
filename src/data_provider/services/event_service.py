from data_provider.repositories.event_repository import IEventRepository

class EventService:
    def __init__(self, event_repository: IEventRepository):
        self.event_repository = event_repository

    def create_event(self, event_data: dict):
        return self.event_repository.save_event(event_data)

    def list_events(self, filters: dict):
        return self.event_repository.get_events(filters)
