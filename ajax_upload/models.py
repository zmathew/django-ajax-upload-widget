from django.db import models
from django.utils.translation import ugettext_lazy as _


class UploadedFile(models.Model):
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    file = models.FileField(_('file'), upload_to='ajax_uploads/')

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
