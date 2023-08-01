import shutil

from django.core.files import File


class FileSaveMixin:
    def save_file(self, path, filename):
        """Saves a file from the given path to a temporary directory and returns a Django File object.

        Reason for this is to avoid `django.core.exceptions.SuspiciousFileOperation` exception.
        """

        shutil.copyfile(path, f"/tmp/{filename}")
        return File(open(f"/tmp/{filename}", "rb"), name=filename)
