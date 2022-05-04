from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
import youtube_dl
from pytube import *
import re


def home(request):
    return render(request, 'index.html')


def download(request):
    url = request.POST['search']
    video = YouTube(url)

    stream = video.streams.all()

    resolution_list = []

    for i in stream:  # get list with all resolutions possible
        if i.resolution is not None:
            resolution_list.append(i.resolution)
    resolution_list = list(dict.fromkeys(resolution_list))  # remove possible duplicates
    resolution_list.sort(reverse=True)
    return render(request, 'download.html', {'resolution_list': resolution_list})


def submit(request):
    url = request.GET['search']

    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(
            url, download=False)
    video_audio_streams = []
    for m in meta['formats']:
        file_size = m['filesize']
        if file_size is not None:
            file_size = f'{round(int(file_size) / 1000000, 2)} mb'

        resolution = 'Audio'
        if m['height'] is not None:
            resolution = f"{m['height']}x{m['width']}"
        video_audio_streams.append({
            'resolution': resolution,
            'extension': m['ext'],
            'file_size': file_size,
            'video_url': m['url']
        })
    video_audio_streams = video_audio_streams[::-1]
    context = {
        'title': meta.get('title', None),
        'streams': video_audio_streams,
        'description': meta.get('description'),
        'likes': f'{int(meta.get("like_count", 0)):,}',
        'dislikes': f'{int(meta.get("dislike_count", 0)):,}',
        'thumb': meta.get('thumbnails')[3]['url'],
        'duration': round(int(meta.get('duration', 1)) / 60, 2),
        'views': f'{int(meta.get("view_count")):,}'
    }

    embed = url.replace('watch?v=', 'embed/')
    # {% extends 'index.html' %}
    return render(request, 'video-list.html')
