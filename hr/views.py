from django.shortcuts import render
from employees.models import HRNotification


def hr_dashboard(request):
    # Fetch all employees with their latest sentiment and team
    employees = SentimentPrediction.objects.select_related('team').order_by('-timestamp')

    # Fetch all HR notifications
    notifications = HRNotification.objects.all().order_by('-timestamp')

    context = {
        'employees': employees,
        'notifications': notifications,
    }
    
    return render(request, 'hr/dashboard.html', context)