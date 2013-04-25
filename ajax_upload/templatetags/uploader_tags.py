from django.conf import settings
from django.template import Library

from ajax_upload import settings as upload_settings

register = Library()


@register.assignment_tag
def get_upload_settings():
    return {
        'max_filesize': getattr(settings, 'AJAX_UPLOAD_MAX_FILESIZE', upload_settings.DEFAULT_MAX_FILESIZE)
    }
