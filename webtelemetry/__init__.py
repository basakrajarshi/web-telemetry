import os
import sys
import imp
import global_settings

class SettingsLoader(object):
    def __init__(self):

        # load global settings
        self._load_settings(global_settings)

        local_settings_file = os.environ.get('WEBTELEMETRY_SETTINGS', None)

        local_settings = None
        if local_settings_file:
            local_settings = imp.load_source('local_settings', local_settings_file)
            self._load_settings(local_settings)

    def _load_settings(self, mod):
        for setting in dir(mod):
            if setting.isupper():
                setattr(self, setting, getattr(mod, setting))

settings = SettingsLoader()

import app
def run_server():
    app.main()
