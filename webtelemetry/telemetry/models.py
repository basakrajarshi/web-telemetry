from __future__ import unicode_literals
from django.db import models

EVENT_CHOICES = (
    ('CLICK', 'click'),
    ('KEYPRESS', 'keypress')
)

class TelemetryItem(models.Model):
    event_type = models.CharField(choices=EVENT_CHOICES, blank=False, max_length=10)
    os = models.CharField(max_length=30, blank=False)
    user_agent = models.CharField(max_length=150, blank=False)
    timestamp = models.DateField(blank=False)
