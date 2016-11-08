from django.conf.urls import url
from views import insert_telemetry_data_view, check_session

urlpatterns = [
    url(r'^insert/', insert_telemetry_data_view),
    url(r'^checksession/', check_session),
]
