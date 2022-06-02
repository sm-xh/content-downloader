from django.forms import ModelForm
from django import forms

import re


class YouTubeForm(forms.Form):
    youtube_url = forms.URLField(label=False,
                                 widget=forms.TextInput(
                                     attrs={'placeholder': '\tPaste youtube url.', 'name': 'search'}),
                                 max_length=47)

    def clean_youtube_url(self):
        data = self.cleaned_data['youtube_url']
        if not YouTubeForm.validate_link(data):
            raise forms.ValidationError('Invalid youtube url', code='invalid')

        return data

    @staticmethod
    def validate_link(url):
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

