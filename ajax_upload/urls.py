try:
    from django.conf.urls import patterns, url, include
except ImportError:
    from django.conf.urls.defaults import patterns, url, include


urlpatterns = patterns('ajax_upload.views',
    url(r'^$', 'upload', name='ajax-upload'),
)
