from django.conf import settings


FILE_FIELD_MAX_LENGTH = getattr(settings, 'AJAX_UPLOAD_FILE_FIELD_MAX_LENGTH', 255)
UPLOAD_TO_DIRECTORY = getattr(settings, 'AJAX_UPLOAD_FILE_TARGET_DIRECTORY', 'ajax_uploads/')
