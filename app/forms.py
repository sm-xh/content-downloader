from django.forms import ModelForm
from .models import YouTubeDownloader
from django import forms

import re


def validate_link(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match

    return youtube_regex_match


class YouTubeLinkForm(ModelForm):
    class Meta:
        model = YouTubeDownloader
        fields = ['youtube_url']


class YouTubeForm(forms.Form):
    youtube_url = forms.CharField(label=False,
                                  widget=forms.TextInput(
                                      attrs={'placeholder': '\tPaste youtube url.', 'name': 'search'}),
                                  max_length=47)

    def clean_youtube_url(self):
        data = self.cleaned_data['youtube_url']
        if not validate_link(data):
            raise forms.ValidationError('Invalid youtube url', code='invalid')

        return data
