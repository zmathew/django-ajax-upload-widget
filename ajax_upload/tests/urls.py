from django.conf.urls import patterns, url

from ajax_upload.urls import urlpatterns


urlpatterns += patterns('ajax_upload.tests.views',
    url(r'^test/$', 'test_view', name='ajax-uploads-test'),
)
