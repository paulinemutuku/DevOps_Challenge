import os
import sys

import django
from coverage import Coverage
from django.test.runner import DiscoverRunner

if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "fitness_booking.settings"
    django.setup()

    print(f"Django settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

    cov = Coverage(source=["booking"])
    cov.start()

    test_runner = DiscoverRunner(verbosity=2)
    failures = test_runner.run_tests(["booking"])

    cov.stop()
    cov.save()
    cov.report()
    cov.xml_report(outfile="coverage.xml")

    sys.exit(bool(failures))
