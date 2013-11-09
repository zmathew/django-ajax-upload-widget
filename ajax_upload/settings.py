from django.conf import settings


FILE_FIELD_MAX_LENGTH = getattr(settings, 'AJAX_UPLOAD_FILE_FIELD_MAX_LENGTH', 255)
