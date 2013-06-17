import uuid

from django import forms

from ajax_upload.models import UploadedFile


class UploadedFileForm(forms.ModelForm):

    class Meta:
        model = UploadedFile
        fields = ('file',)

    def clean_file(self):
        data = self.cleaned_data['file']
        # Change the name of the file to something unguessable
        # Construct the new name as <unique-hex>-<original>.<ext>
        data.name = u'%s-%s' % (uuid.uuid4().hex, data.name)
        return data
