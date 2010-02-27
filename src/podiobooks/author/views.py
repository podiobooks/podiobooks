"""
    Views for the Author module
"""
from django.conf import settings
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from podiobooks.author.audio_validation import validate_mp3
import os

class UploadFileForm(forms.Form):
    """Simple form to handle uploading the mp3 file for authors"""
    file = forms.FileField()

def handle_uploaded_file(f, destination_file_name):
    """Handles the uploaded file data chunks"""
    destination = open(destination_file_name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

#@login_required
def upload(request):
    """
    Test Upload Page

    url: /author/upload
    
    template : author/templates/upload_form.html
    """
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploadedFile = request.FILES['file']
            destinationFileName = settings.PROJECT_PATH + '/media/uploads/mp3validation' + uploadedFile.name
            handle_uploaded_file(uploadedFile, destinationFileName)
            validation_results = validate_mp3(destinationFileName)
            os.remove(destinationFileName)
            response_data = {'results': validation_results, 'fileName': destinationFileName}
            return render_to_response('author/upload_results.html', response_data, context_instance=RequestContext(request))
    else:
        form = UploadFileForm()
    return render_to_response('author/upload_form.html', {'form': form}, context_instance=RequestContext(request))
