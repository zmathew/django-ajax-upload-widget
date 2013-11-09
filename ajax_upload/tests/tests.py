import os

from django.conf import settings
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from django.utils import simplejson
from django.utils.translation import ugettext as _

from ajax_upload.models import UploadedFile
from ajax_upload.widgets import AjaxUploadException


TEST_FILEPATH = os.path.dirname(__file__) + '/files/test.png'


class UploaderTestHelper(object):

    def tearDown(self):
        # Delete all uploaded files created during testing
        for up in UploadedFile.objects.all():
            if up.file:
                up.file.delete()

    def create_uploaded_file(self, **kwargs):
        defaults = {
            'file': 'test.png'
        }
        defaults.update(kwargs)
        return UploadedFile.objects.create(**defaults)


class AjaxUploadTests(UploaderTestHelper, TestCase):

    def test_upload_file_submission_saves_file_with_different_name_and_returns_json(self):
        post_data = {
            'file': open(TEST_FILEPATH)
        }
        response = self.client.post(reverse('ajax-upload'), post_data)
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        uploaded_file = UploadedFile.objects.get()
        self.assertTrue(os.path.exists(uploaded_file.file.path))
        self.assertEqual(json['path'], uploaded_file.file.url)
        # This is a not-so-good test to verify that the filename name is modified
        self.assertTrue(len(os.path.basename(uploaded_file.file.name)) > 16)

    def test_upload_file_submission_missing_file_returns_error(self):
        post_data = {
            'file': ''
        }
        response = self.client.post(reverse('ajax-upload'), post_data)
        self.assertEqual(response.status_code, 400)
        json = simplejson.loads(response.content)
        self.assertTrue('errors' in json)
        self.assertEqual(json['errors']['file'][0], _('This field is required.'))

    def test_upload_file_get_request_returns_405(self):
        response = self.client.get(reverse('ajax-upload'))
        self.assertEqual(response.status_code, 405)


class AjaxFileInputTests(UploaderTestHelper, TestCase):
    urls = 'ajax_upload.tests.urls'

    def test_submit_form_with_uploaded_file_path(self):
        # First ajax upload the file to the uploader
        post_data = {
            'file': open(TEST_FILEPATH)
        }
        response = self.client.post(reverse('ajax-upload'), post_data)
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        uploaded_file = UploadedFile.objects.get()
        self.assertTrue(os.path.exists(uploaded_file.file.path))

        # Now submit the original form with the path of the uploaded file
        post_data = {
            'my_file': json['path'],
            'my_image': json['path']  # We're testing both AjaxFileField and AjaxImageField
        }
        response = self.client.post(reverse('ajax-uploads-test'), post_data)
        self.assertEqual(response.status_code, 200)
        parsed = simplejson.loads(response.content)
        self.assertEqual(parsed['uploaded_file_name'], json['path'].replace(settings.MEDIA_URL, ''))
        self.assertEqual(parsed['uploaded_image_name'], json['path'].replace(settings.MEDIA_URL, ''))

    def test_submit_form_with_empty_path_clears_existing_file(self):
        post_data = {
            'my_file': '',
            'my_image': ''
        }
        response = self.client.post(reverse('ajax-uploads-test'), post_data)
        self.assertEqual(response.status_code, 200)
        parsed = simplejson.loads(response.content)
        self.assertEqual(parsed['uploaded_file_name'], 'False')
        self.assertEqual(parsed['uploaded_image_name'], 'False')

    def test_submit_form_with_external_file_path_returns_error(self):
        post_data = {
            'my_file': 'http://www.google.com/invalid.txt',
            'my_image': 'http://www.google.com/invalid.png'
        }
        try:
            self.client.post(reverse('ajax-uploads-test'), post_data)
        except AjaxUploadException, err:
            self.assertTrue(str(err).startswith(_('File path not allowed:')))
        else:
            self.fail()

    def test_submit_form_with_internal_file_path_ignores_it_and_retains_original_value(self):
        # In this scenario, we're simulating the submission of an form that had
        # an existing file specified and didn't change/ajax upload it (eg. an update form).
        post_data = {
            'my_file': '%ssome/INVALID-path/file.txt' % settings.MEDIA_URL,  # invalid path
            'my_image': '%ssome/path/image.png' % settings.MEDIA_URL  # valid path
            # We ignore BOTH valid and invalid paths to prevent the user from setting
            # the value to a file that they did not upload
        }
        response = self.client.post(reverse('ajax-uploads-test'), post_data)
        self.assertEqual(response.status_code, 200)
        parsed = simplejson.loads(response.content)
        self.assertEqual(parsed['uploaded_file_name'], 'some/path/file.txt')
        self.assertEqual(parsed['uploaded_image_name'], 'some/path/image.png')

    def test_submit_form_normally_with_file_data_in_multipart_format(self):
        # Here we will NOT use the AJAX uploader to ensure the file field works normally.
        post_data = {
            'my_file': open(TEST_FILEPATH),
            'my_image': open(TEST_FILEPATH)
        }
        response = self.client.post(reverse('ajax-uploads-test'), post_data)
        self.assertEqual(response.status_code, 200)
        parsed = simplejson.loads(response.content)
        self.assertTrue('errors' not in parsed)
        self.assertTrue('uploaded_file_name' in parsed)
        self.assertTrue('uploaded_image_name' in parsed)
