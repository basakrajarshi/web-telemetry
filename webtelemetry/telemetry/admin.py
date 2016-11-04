from django.contrib import admin
from telemetry.models import TelemetryItem


class TelemetryItemAdmin(admin.ModelAdmin):
    def view_timestamp(self, obj):
        return obj.timestamp.ctime()

    list_display = ('id', 'event_type', 'os', 'view_timestamp', 'element')


admin.site.register(TelemetryItem, TelemetryItemAdmin)
