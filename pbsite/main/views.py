from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login

def index(request):
    return render_to_response('main/index.html', {})
