from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.core.exceptions import ValidationError

import json
from datetime import datetime
from uuid import uuid4

from models import TelemetryItem
from exceptions import InvalidSessionException, InvalidTelemetryDataException

def _create_telemetry_session():
    return uuid4().hex

@require_http_methods(['POST'])
@csrf_exempt
def insert_telemetry_data_view(request):
    if request.method == 'POST':
        telemetry_data = request.body

        if not telemetry_data:
            raise InvalidTelemetryDataException('No Telemetry Data present')

        telemetry_data = json.loads(telemetry_data)['telemetry']

        # get the session information
        telemetry_session_id = request.session.get('telemetry_session', None)
        if not telemetry_session_id:
            raise InvalidSessionException('Invalid Telemetry Session')

        # for each telemetry item
        # construct the model object
        for item in telemetry_data:

            # parse datetime
            if not item['timestamp']:
                raise InvalidTelemetryDataException('No/Invalid timestamp specified')
            timestamp = datetime.strptime(item['timestamp'], '%m/%d/%Y, %I:%M:%S %p')

            telemetry_item = TelemetryItem(
                event_type=item['type'],
                os=item['os'],
                user_agent=item['userAgent'],
                timestamp=timestamp,
                element=item['element'],
                session_id=telemetry_session_id
            )
            try:
                telemetry_item.full_clean()
            except ValidationError as e:
                print e
                return JsonResponse({
                    'message': e.message
                }, status=400)
            telemetry_item.save()
        return JsonResponse({})

@require_http_methods(['POST'])
@csrf_exempt
def check_session(request):
    session_cookie = request.session.get('telemetry_session', None)
    # if session cookie exists, return blank JSON Response
    if session_cookie:
        print 'cookie exists. returning'
        return HttpResponse(json.dumps({}))
    # create a session
    telemetry_id = _create_telemetry_session()
    request.session['telemetry_session'] = telemetry_id
    return HttpResponse(json.dumps({}))
