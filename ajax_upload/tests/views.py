from django.http import HttpResponse, HttpResponseBadRequest
try:
    import json
except ImportError:
    from django.utils import simplejson as json

from ajax_upload.tests.forms import TestForm


def test_view(request):
    form = TestForm(data=request.POST, files=request.FILES, initial={
        'my_file': 'some/path/file.txt',
        'my_image': 'some/path/image.png',
    })
    if form.is_valid():
        data = {
            'uploaded_file_name': str(form.cleaned_data['my_file']),
            'uploaded_image_name': str(form.cleaned_data['my_image'])
        }
        return HttpResponse(
            json.dumps(data), content_type="application/json; charset=utf-8"
        )
    else:
        return HttpResponseBadRequest(
            json.dumps({'errors': form.errors}),
            content_type="application/json; charset=utf-8"
        )
