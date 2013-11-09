from django.db import models
from django.utils.translation import ugettext_lazy as _

from ajax_upload.settings import FILE_FIELD_MAX_LENGTH


class UploadedFile(models.Model):
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    file = models.FileField(_('file'), max_length=FILE_FIELD_MAX_LENGTH, upload_to='ajax_uploads/')

    class Meta:
        ordering = ('id',)
        verbose_name = _('uploaded file')
        verbose_name_plural = _('uploaded files')

    def __unicode__(self):
        return unicode(self.file)

    def delete(self, *args, **kwargs):
        super(UploadedFile, self).delete(*args, **kwargs)
        if self.file:
            self.file.delete()
    delete.alters_data = True
