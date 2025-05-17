from django.db import models

# HR Model for Historical Mood Tracking
class HistoricalMood(models.Model):
    employee_id = models.CharField(max_length=10)
    sentiment = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.employee_id} - {self.sentiment}'
