import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from ajax_upload.forms import UploadedFileForm
fromt ajax_upload.settings import UPLOAD_PERMISSION_CHECKER as permission_checker

@csrf_exempt
@require_POST
def upload(request):
    if callable(permission_checker):
        errors = permission_checker(request)
        if errors is not None:
            return HttpResponseBadRequest(json.dumps(errors))
    form = UploadedFileForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        uploaded_file = form.save()
        data = {
            'path': uploaded_file.file.url,
        }
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponseBadRequest(json.dumps({'errors': form.errors}))
