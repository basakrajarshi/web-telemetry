from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

@require_http_methods(['POST'])
def insert_telemetry_data_view(request):
    if request.method == 'POST':
        pass
