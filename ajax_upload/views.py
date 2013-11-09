from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from ajax_upload.forms import UploadedFileForm


@csrf_exempt
@require_POST
def upload(request):
    form = UploadedFileForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        uploaded_file = form.save()
        data = {
            'path': uploaded_file.file.url,
        }
        return HttpResponse(json.dumps(data), content_type="application/json; charset=utf-8")
    else:
        return HttpResponseBadRequest(json.dumps({'errors': form.errors}),
                                      content_type="application/json; charset=utf-8")
