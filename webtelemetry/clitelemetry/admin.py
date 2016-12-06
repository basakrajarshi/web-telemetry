from django.contrib import admin

from clitelemetry.models import Session
from clitelemetry.models import Event


# Register your models here.
class EventInline(admin.TabularInline):
    model = Event

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    inlines = [EventInline,]

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
