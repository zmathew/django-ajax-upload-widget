from django.conf.urls import url
from ajax_upload.views import upload


urlpatterns = [
    url(r'^$', upload, name='ajax-upload'),
]
