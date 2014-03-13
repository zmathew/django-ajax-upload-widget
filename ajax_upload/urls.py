try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('ajax_upload.views',
    url(r'^$', 'upload', name='ajax-upload'),
)
