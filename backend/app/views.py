import mimetypes
import os

import pytube.metadata
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
import youtube_dl
from pytube import *
import re
pytube.metadata.YouTubeMetadata
video_url = ''


def home(request):
    return render(request, 'index.html')


def settings(request):
    global video_url
    video_url = request.POST['search']
    video = YouTube(video_url)

    stream = video.streams
    resolution_list = []

    for i in stream:  # get list with all resolutions possible
        if i.resolution is not None:
            resolution_list.append(i.resolution)
    resolution_list = list(dict.fromkeys(resolution_list))  # remove possible duplicates
    resolution_list.sort(reverse=True)
    return render(request, 'download.html', {'resolution_list': resolution_list, 'url': video_url})


def download(request):
    global video_url
    file_format = request.POST['select_format']
    resolution = request.POST['resolution']
    metadata_status = request.POST.get('meta', 'off')
    vid = YouTube(video_url)

    if metadata_status=='on':
        metadata = {"title": vid.title, "author": vid.author, "description": vid.description,
                    "publish_date": str(vid.publish_date), "keywords": vid.keywords, "length": vid.length,
                    "views": vid.views}
        # Writing to file
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open("metadata.json", "w") as file1:
            # Writing data to a file
            file1.write(str(metadata))
        # Define text file name
        filename = 'metadata.json'
        # Define the full file path
        filepath = BASE_DIR + "\\" + filename
        # Open the file for reading content
        path = open(filepath, 'r')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename

    if file_format == "Video":
        vid.streams.filter(res=resolution).first().download()
    elif file_format == "Audio":
        vid.streams.filter(only_audio=True).first().download()

    return render(request, 'index.html')
