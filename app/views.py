from django.http import HttpResponse
from django.shortcuts import render

import mimetypes
import os
import pytube.metadata
from pathlib import Path
from pytube import *
import ffmpeg
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
    print(video_url)
    file_format = request.POST['select_format']
    metadata_status = request.POST.get('meta', 'off')
    vid = YouTube(video_url)

    filespath = os.path.join(BASE_DIR, 'files/')

    if metadata_status == 'on':
        metadata = {"title": vid.title, "author": vid.author, "description": vid.description,
                    "publish_date": str(vid.publish_date), "keywords": vid.keywords, "length": vid.length,
                    "views": vid.views}
        # Writing to file
        filename = 'metadata.json'
        with open(filespath+filename, "w") as file1:
            # Writing data to a file
            file1.write(str(metadata))

        # Open the file for reading content
        path = open(filespath+filename, 'r')
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type="application/json")
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        path.close()
        os.remove(filespath+filename)

        # todo: change metadata to seperate download button
        return response

    if file_format == "Video":
        resolution = request.POST['resolution']
        vid.streams.filter(res=resolution).first().download(filespath)
        filename = vid.title + ".mp4"

    elif file_format == "Audio":
        vid.streams.filter(only_audio=True).first().download(filespath)
        # running ffmpeg on downloaded file
        filename_mp4 = filespath+vid.title+".mp4"
        filename_mp3 = filespath+vid.title+".mp3"
        cmd = "ffmpeg -i {} -vn {}".format(filename_mp4, filename_mp3)
        subprocess.call("ffmpeg -i {} -vn {}".format(filename_mp4, filename_mp3))
        # changing filename
        p = Path(filespath+vid.title+'.mp4')
        p.rename(p.with_suffix('.mp3'))
        filename = vid.title + ".mp3"

    #mime_type, _ = mimetypes.guess_type("files\\"+filespath)
    path = open(filespath+filename, 'rb')
    # Set the return value of the HttpResponse
    if file_format == "Video":
        response = HttpResponse(path, content_type="video/mp4")
    elif file_format == "Audio":
        response = HttpResponse(path, content_type="audio/mpeg")
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    path.close()
    os.remove(filespath+filename)
    return response
