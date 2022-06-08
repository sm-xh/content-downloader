from django.forms import ModelForm
from django import forms
from pytube import YouTube
from pytube import exceptions

import re


class YouTubeURLForm(forms.Form):
    youtube_url = forms.URLField(label=False,
                                 widget=forms.TextInput(
                                     attrs={'placeholder': 'Paste youtube url.', 'name': 'search'}),
                                 max_length=47)

    def clean_youtube_url(self):
        data = self.cleaned_data['youtube_url']
        try:
            video = YouTube(data).streams
        except exceptions.PytubeError as err:
            raise forms.ValidationError(err, code='invalid_url')

        return data

    @staticmethod
    def validate_link(url):
        # 1st check if url is youtube url
        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

        youtube_regex_match = re.match(youtube_regex, url)

        if youtube_regex_match:
            return youtube_regex_match

        return youtube_regex_match


class YouTubeDownloadForm(forms.Form):
    class Meta:
        fields = []

    select_format = forms.ChoiceField(widget=forms.Select, choices=[('Video', 'Video'), ('Audio', 'Audio')])
    select_resolution = forms.ChoiceField(widget=forms.Select)
    select_metadata = forms.BooleanField(widget=forms.CheckboxInput, required=False)

    def __init__(self, res_list, *args, **kwargs):
        super(YouTubeDownloadForm, self).__init__(*args, **kwargs)
        self.fields['select_resolution'] = forms.ChoiceField(choices=res_list)

    def clean_select_format(self):
        data = self.cleaned_data['select_format']
        allowed_formats = ['Audio', 'Video']
        if data not in allowed_formats:
            raise forms.ValidationError("invalid format", code='invalid_format')

        return data

    def clean_select_resolution(self):
        data = self.cleaned_data['select_resolution']
        #  [('1080p', '1080p'), ('440p', '440p'), ('144p', '144p'), ('2160p', '2160p'),
        #                       ('240p', '240p'),
        #                       ('360p', '360p'), ('480p', '480p'), ('720p', '720p')]
        allowed_resolution = ['1080p', '440p', '144p', '2160p', '240p', '360p', '480p', '720p']

        if data not in allowed_resolution:
            raise forms.ValidationError("invalid resolution", code='invalid_resolution')
