from django.http import HttpResponse
from django.shortcuts import render
from django_content_downloader.settings import BASE_DIR
from .forms import YouTubeForm

import mimetypes
import os
import pytube.metadata
from pathlib import Path
from os.path import basename
from pytube import *
from zipfile import ZipFile

import ffmpeg
import subprocess

video_url = ''


def home(request):
    form = YouTubeForm
    context = {'form': form}
    return render(request, 'index.html', context)


def settings(request):
    global video_url
    if request.method == 'POST':
        form = YouTubeForm(request.POST)
        if form.is_valid():

            video_url = form.cleaned_data['youtube_url']
            video = YouTube(video_url)

            stream = video.streams
            resolution_list = []

            for i in stream:  # get list with all resolutions possible
                if i.resolution is not None:
                    resolution_list.append(i.resolution)
            resolution_list = list(dict.fromkeys(resolution_list))  # remove possible duplicates
            resolution_list.sort(reverse=True)
            return render(request, 'download.html', {'resolution_list': resolution_list, 'url': video_url})

    else:
        form = YouTubeForm()

    context = {'form': form}

    return render(request, 'index.html', context)




def download(request):
    global video_url

    filespath = os.path.dirname(os.path.abspath(__file__))
    filespath = os.path.join(BASE_DIR, "/app/files/")

    filename = "downloaded"

    file_format = request.POST['select_format']
    metadata_status = request.POST.get('meta', 'off')
    vid = YouTube(video_url)

    print(filespath)

    # section for downloading the file
    if file_format == "Video":
        ext = ".mp4"
        filename = "filename" + ".mp4"
        resolution = request.POST['resolution']
        vid.streams.filter(res=resolution).first().download(output_path=filespath, filename=filename)

    elif file_format == "Audio":
        ext = ".mp3"
        filename = "filename" + ".mp3"
        vid.streams.filter(only_audio=True).first().download(output_path=filespath, filename=filename)

    if metadata_status == 'on':
        metadata = {"title": vid.title, "author": vid.author, "description": vid.description,
                    "publish_date": str(vid.publish_date), "keywords": vid.keywords, "length": vid.length,
                    "views": vid.views}
        # Writing to file
        meta_name = 'metadata.json'
        with open(filespath + meta_name, "w") as file1:
            # Writing data to a file
            file1.write(str(metadata))

        zip_name = 'content.zip'
        zipObj = ZipFile(filespath + zip_name, 'w')

        # Add multiple files to the zip
        zipObj.write(filespath + meta_name, basename(filespath + meta_name))
        zipObj.write(filespath + filename, basename(filespath + filename))
        zipObj.close()

        # Open the file for reading content
        path = open(filespath + 'content.zip', 'rb')
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type='application/x-zip-compressed')

        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % zip_name

        path.close()
        os.remove(filespath + meta_name)
        os.remove(filespath + zip_name)
        os.remove(filespath + filename)

        # todo: change metadata to seperate download button
        return response
    else:
        path = open(filespath + filename, 'rb')
        # Set the return value of the HttpResponse
        if file_format == "Video":
            response = HttpResponse(path, content_type="video/mp4")
        elif file_format == "Audio":
            response = HttpResponse(path, content_type="audio/mpeg")
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % (vid.title + ext)
        path.close()
        os.remove(filespath + filename)
        return response
