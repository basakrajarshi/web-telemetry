from __future__ import unicode_literals
from django.db import models

EVENT_CHOICES = (
    ('click', 'click'),
    ('keypress', 'keypress'),
    ('navigation', 'navigation'),
    ('scrollend', 'scrollend'),
    ('focus', 'focus'),
    ('blur', 'blur'),
    ('error', 'error')
)

class TelemetryItem(models.Model):
    event_type = models.CharField(choices=EVENT_CHOICES, blank=False, max_length=10)
    os = models.CharField(max_length=30, blank=False)
    user_agent = models.CharField(max_length=150, blank=False)
    timestamp = models.DateTimeField(blank=False)
    element = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=100, blank=False)
    new_location = models.CharField(max_length=100, blank=True)
    session_id = models.CharField(max_length=32, blank=False)
    error_message = models.CharField(max_length=75, blank=True)
    error_line_no = models.CharField(max_length=10, blank=True)
