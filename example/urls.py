from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

try:
    from django.conf.urls import patterns, url, include
except ImportError:
    from django.conf.urls.defaults import patterns, url, include

admin.autodiscover()

urlpatterns = patterns('example.views',
    url(r'^add/$', 'add_edit_product', name='example-add-product'),
    url(r'^edit/(?P<product_id>\d+)/$', 'add_edit_product', name='example-edit-product'),
    url(r'^upload/', include('ajax_upload.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT, 'show_indexes': True
    }),
)

urlpatterns += staticfiles_urlpatterns()