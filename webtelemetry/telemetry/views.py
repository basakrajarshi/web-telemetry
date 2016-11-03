from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.core.exceptions import ValidationError

from models import TelemetryItem
from exceptions import InvalidTelemetryDataException


@require_http_methods(['POST'])
@csrf_exempt
def insert_telemetry_data_view(request):
    if request.method == 'POST':
        telemetry_data = request.POST.getlist('telemetry', None)

        if not telemetry_data:
            raise InvalidTelemetryDataException('No Telemetry Data present')

        # for each telemetry item
        # construct the model object
        for item in telemetry_data:
            telemetry_item = TelemetryItem(
                event_type=item['event_type'],
                os=item['os'],
                user_agent=item['user_agent'],
                timestamp=item['timestamp']
            )
            try:
                telemetry_item.full_clean()
            except ValidationError as e:
                return JsonResponse({
                    'code': e.code,
                    'message': e.message
                }, status=400)
            telemetry_item.save()
        return JsonResponse({})
