class TelemetryDataException(Exception):
    """Base class for any Telemetry data Errors"""
    pass

class InvalidTelemetryDataException(TelemetryDataException):
    """Telemetry data is not valid"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
