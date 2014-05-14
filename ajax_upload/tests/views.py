import json

from django.http import HttpResponse, HttpResponseBadRequest

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
            json.dumps(data), content_type='application/json'
        )
    else:
        return HttpResponseBadRequest(
            json.dumps({'errors': form.errors}),
            content_type='application/json'
        )
