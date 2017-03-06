import unittest
import os

def get_test_suite():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(current_dir, 'tests')

    telemetry_test_suite = unittest.TestSuite()

    try:
        app_suite = unittest.TestLoader().discover(test_dir)
        telemetry_test_suite.addTests(app_suite)
    except ImportError as e:
        print "No tests found"

    return telemetry_test_suite


if __name__ == '__main__':
    suite = get_test_suite()
    unittest.TextTestRunner().run(suite)
