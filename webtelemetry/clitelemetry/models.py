from __future__ import unicode_literals

from django.db import models
import uuid

# Create your models here.
class Session(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4,editable=False)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    user = models.CharField(max_length=24)
    terminal = models.CharField(max_length=24)
    host = models.CharField(max_length=32)

class Event(models.Model):
    session = models.ForeignKey(Session)
    audit_id = models.IntegerField()
    cwd = models.CharField(max_length=1024)
    time = models.DateTimeField()
    cmd = models.CharField(max_length=1024)
    exit = models.CharField(max_length=48)
    success = models.BooleanField()
