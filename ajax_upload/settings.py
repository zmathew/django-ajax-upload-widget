from django.conf import settings


# Number of seconds to keep uploaded files. The clean_uploaded command will
# delete them after this has expired.
UPLOADER_DELETE_AFTER = getattr(settings, 'UPLOADER_DELETE_AFTER', 60 * 60)
DEFAULT_MAX_FILESIZE = 0
FILE_FIELD_MAX_LENGTH = getattr(settings, 'AJAX_UPLOAD_FILE_FIELD_MAX_LENGTH', 255)
