from django.contrib import admin
from .models import SentimentPrediction, HRNotification, Team

# Register models
admin.site.register(SentimentPrediction)
admin.site.register(HRNotification)
admin.site.register(Team)

