from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from app.views import home, settings, download
from app.forms import YouTubeDownloadForm, YouTubeURLForm
from selenium import webdriver


# Create your tests here.

# test urls.py
class TestUrls(SimpleTestCase):
    def test_list_url_is_resolved(self):
        url = reverse('homepage')
        self.assertEquals(resolve(url).func, home)

    def test_settings_url_is_resolved(self):
        url = reverse('settings')
        self.assertEquals(resolve(url).func, settings)

    def test_download_url_is_resolved(self):
        url = reverse('download')
        self.assertEquals(resolve(url).func, download)


# test forms.py
class TestViews:
    pass


class TestYouTubeURLForm(SimpleTestCase):
    def test_valid_form(self):
        form = YouTubeURLForm(data={'youtube_url': 'https://www.youtube.com/watch?v=jNQXAC9IVRw'})
        self.assertTrue(form.is_valid())

    def test_invalid_form_empty_form(self):
        form = YouTubeURLForm()
        self.assertFalse(form.is_valid())

    def test_invalid_form_invalid_yt_url(self):
        form = YouTubeURLForm(data={'youtube_url': 'https://www.youtube.com/watch?v=jNQXAC9IVR2'})
        self.assertFalse(form.is_valid())

    def test_invalid_form_private_yt_url(self):
        form = YouTubeURLForm(data={'youtube_url': 'https://www.youtube.com/0vmNFSo8bq0'})
        self.assertFalse(form.is_valid())

    def test_invalid_form_not_yt_url(self):
        form = YouTubeURLForm(data={'youtube_url': 'https://www.google.com/'})
        self.assertFalse(form.is_valid())

    def test_invalid_form_empty_url(self):
        form = YouTubeURLForm(data={'youtube_url': ''})
        self.assertFalse(form.is_valid())


class TestYouTubeDownloadForm(SimpleTestCase):
    res_list = [('1080p', '1080p'), ('440p', '440p'), ('144p', '144p'), ('2160p', '2160p'), ('240p', '240p'),
                ('360p', '360p'), ('480p', '480p'), ('720p', '720p')]

    def test_valid_video_form(self):
        form = YouTubeDownloadForm(self.res_list, data={'select_format': 'Video', 'select_resolution': '1080p'})
        self.assertTrue(form.is_valid())

    def test_valid_audio_form(self):
        form = YouTubeDownloadForm(self.res_list, data={'select_format': 'Audio', 'select_resolution': '1080p'})
        self.assertTrue(form.is_valid())

    def test_invalid_form_empty_form(self):
        form = YouTubeDownloadForm(self.res_list)
        self.assertFalse(form.is_valid())

    def test_invalid_form_missing_resolution(self):
        form = YouTubeDownloadForm(self.res_list, data={'select_format': 'XYZ'})
        self.assertFalse(form.is_valid())

    def test_invalid_form_private_yt_url(self):
        form = YouTubeDownloadForm(self.res_list, data={'select_format': 'Video', 'select_resolution': '1080p'})
        self.assertFalse(form.is_valid())

    def test_invalid_form_not_yt_url(self):
        form = YouTubeDownloadForm(self.res_list, data={'select_format': 'Video', 'select_resolution': '1080p'})
        self.assertFalse(form.is_valid())

    def test_invalid_form_empty_url(self):
        form = YouTubeDownloadForm(self.res_list, data={'select_format': 'Video', 'select_resolution': '1080p'})
        self.assertFalse(form.is_valid())


class TestInvalidYouTubeUrl:
    pass


class TestMp3FileDownload:
    pass


class TestMp4FileDownload:
    pass


class TestMp3ZipDownload:
    pass


class TestMp4ZipDownload:
    pass


class TestDownload:
    pass


class TestWholeFlow:
    pass
