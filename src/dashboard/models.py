from django.db import models

class Dashboard(models.Model):
    hotel_id = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField(null=True, blank=True)  # Nullable for daily aggregation
    day = models.DateField(null=True, blank=True)  # Nullable for monthly aggregation
    bookings_count = models.IntegerField()  # The count of bookings for that period

    class Meta:
        unique_together = ('hotel_id', 'year', 'month', 'day')  # Ensure uniqueness per hotel-year-month-day combination

    def __str__(self):
        period = f"{self.year}-{self.month or 'All'}-{self.day or 'All'}"
        return f"Hotel {self.hotel_id} - {period}: {self.bookings_count} bookings"

class ProcessedDateRange(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    processed_at = models.DateTimeField(auto_now_add=True)  # When the range was processed

    class Meta:
        unique_together = ('start_date', 'end_date')  # Ensure unique date ranges

    def __str__(self):
        return f"Processed from {self.start_date} to {self.end_date}"
