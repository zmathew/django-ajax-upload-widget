from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from .models import UploadedFile


class AjaxUploadException(Exception):
    pass


class AjaxClearableFileInput(forms.ClearableFileInput):
    template_with_clear = ''  # We don't need this
    template_with_initial = '%(input)s'

    def render(self, name, value, attrs=None):
        attrs = attrs or {}
        if value:
            filename = u'%s%s' % (settings.MEDIA_URL, value)
        else:
            filename = ''
        attrs.update({
            'class': attrs.get('class', '') + 'ajax-upload',
            'data-filename': filename,  # This is so the javascript can get the actual value
            'data-required': self.is_required or '',
            'data-upload-url': reverse('ajax-upload')
        })
        output = super(AjaxClearableFileInput, self).render(name, value, attrs)
        return mark_safe(output)

    def value_from_datadict(self, data, files, name):
        # If a file was uploaded or the clear checkbox was checked, use that.
        file = super(AjaxClearableFileInput, self).value_from_datadict(data, files, name)
        if file is not None:  # file may be False - which indicates "clearing" of the field
            return file
        elif name in data:  # This means a file path was specified in the POST field
            file_path = data.get(name)
            if not file_path:
                return False  # False means clear the existing file

            if file_path.startswith(settings.MEDIA_URL):
                # Strip and media url if present
                relative_path = file_path[len(settings.MEDIA_URL):]
            else:
                relative_path = file_path

            try:
                uploaded_file = UploadedFile.objects.get(file=relative_path)
            except UploadedFile.DoesNotExist:
                raise AjaxUploadException(u'%s %s' % (_('Invalid file path:'), file_path))
            else:
                return uploaded_file.file

        return None
