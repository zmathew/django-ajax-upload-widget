from django.conf import settings


FILE_FIELD_MAX_LENGTH = getattr(settings, 'AJAX_UPLOAD_FILE_FIELD_MAX_LENGTH', 255)
FILE_FIELD_ACCEPT_TYPES = getattr(settings, 'AJAX_UPLOAD_FILE_FIELD_ACCEPT_TYPES', None)

