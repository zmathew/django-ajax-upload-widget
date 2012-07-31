from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('example.views',
    url(r'^add/$', 'add_edit_product', name='example-add-product'),
    url(r'^edit/(?P<product_id>\d+)/$', 'add_edit_product', name='example-edit-product'),
)
