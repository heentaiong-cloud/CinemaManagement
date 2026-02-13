from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import time


class Command(BaseCommand):
    help = "Upload a small test file to the configured storage and print results."

    def handle(self, *args, **options):
        name = f"cinema_s3_test_{int(time.time())}.txt"
        content = ContentFile(b"ok")
        self.stdout.write("Using storage: %s" % default_storage.__class__)
        try:
            path = default_storage.save(name, content)
            url = default_storage.url(path)
            exists = default_storage.exists(path)
            self.stdout.write("Saved test file: %s" % path)
            self.stdout.write("URL: %s" % url)
            self.stdout.write("Exists: %s" % exists)
            # Clean up
            try:
                default_storage.delete(path)
                self.stdout.write("Deleted test file: %s" % path)
            except Exception as e:
                self.stderr.write("Failed to delete test file: %s" % e)
        except Exception as exc:
            self.stderr.write("Storage test failed: %s" % exc)
