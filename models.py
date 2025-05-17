from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SentimentPrediction(models.Model):
    employee_id = models.CharField(max_length=10)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='predictions')  # Add related_name
    sentiment = models.CharField(max_length=20)
    task_recommendation = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_id} - {self.team.name} - {self.sentiment}"



class HRNotification(models.Model):
    employee_id = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.employee_id} - {self.message[:30]}...'  
