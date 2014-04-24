import uuid
import os

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from ajax_upload.models import UploadedFile
from . import settings as upload_settings


class UploadedFileForm(forms.ModelForm):

    if getattr(settings, 'AJAX_UPLOAD_USE_IMAGE_FIELD', False):
        file = forms.ImageField()

    ERRORS = {
        'max_filesize': _('The file is bigger than the maximum size allowed.'),
    }

    class Meta:
        model = UploadedFile
        fields = ('file',)

    def clean_file(self):
        data = self.cleaned_data['file']
        # Change the name of the file to something unguessable
        # Construct the new name as <unique-hex>-<original>.<ext>
        original_name, ext = os.path.splitext(data.name)
        data.name = u'%s-%s%s' % (uuid.uuid4().hex, original_name[:32], ext[:4])

        max_upload_size = getattr(settings, 'AJAX_UPLOAD_MAX_FILESIZE', upload_settings.DEFAULT_MAX_FILESIZE)
        if 0 < max_upload_size < data.size:
            raise forms.ValidationError(self.ERRORS['max_filesize'])

        return data
