import unittest
import mock
import os
import tempfile

from webtelemetry import settings as global_settings
from webtelemetry import SettingsLoader

class SettingsLoaderTestCase(unittest.TestCase):
        def test_settings_default(self):
            settings = SettingsLoader()
            self.assertEqual(settings.REDIS_PORT, global_settings.REDIS_PORT)
            self.assertEqual(settings.REDIS_HOST, global_settings.REDIS_HOST)
            self.assertEqual(settings.COOKIE_SECRET, global_settings.COOKIE_SECRET)
