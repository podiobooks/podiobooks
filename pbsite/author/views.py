"""
    Views for the Author module
"""
from django.conf import settings
from django import forms
from django.shortcuts import render_to_response
from django.template import Context
from audio_validation import validate_mp3

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()

def handle_uploaded_file(f, destinationFileName):
    destination = open(destinationFileName, 'wb+')
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
            destinationFileName = settings.PROJECT_PATH + '/author/uploads/' + uploadedFile.name
            handle_uploaded_file(uploadedFile, destinationFileName)
            validation_results = validate_mp3(destinationFileName)
            resultContext = Context({'results': validation_results, 'fileName': destinationFileName})
            return render_to_response('author/upload_results.html', resultContext)
    else:
        form = UploadFileForm()
    return render_to_response('author/upload_form.html', {'form': form})