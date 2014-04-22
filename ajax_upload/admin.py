from django.contrib import admin

from ajax_upload.models import UploadedFile


class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    date_hierarchy = 'creation_date'
    search_fields = ('file',)


admin.site.register(UploadedFile, UploadedFileAdmin)
