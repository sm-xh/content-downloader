from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
import youtube_dl
import re


def home(request):
    return render(request, 'index.html')

def submit(request):
    url = request.GET['search']
    emb = url.replace('watch?v=', 'emb/')
    return render(request, 'video-list.html', {'url': url})