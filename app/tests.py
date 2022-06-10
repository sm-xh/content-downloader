import time

from django.test import TestCase, SimpleTestCase, Client, RequestFactory, LiveServerTestCase
from django.urls import reverse, resolve
from app.views import home, settings, download
from app.forms import YouTubeDownloadForm, YouTubeURLForm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os


# Create your tests here.

# ------------ testing urls.py --------------------
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


# ------------ testing forms.py --------------------

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
        form = YouTubeDownloadForm(self.res_list, data={'select_format': 'Audio', 'select_resolution': '1080p'})
        self.assertTrue(form.is_valid())

    def test_valid_audio_form(self):
        form = YouTubeDownloadForm(self.res_list, data={'select_format': 'Audio', 'select_resolution': '1080p'})
        self.assertTrue(form.is_valid())

    def test_invalid_form_empty_form(self):
        form = YouTubeDownloadForm(self.res_list)
        self.assertFalse(form.is_valid())

    def test_invalid_form_missing_resolution(self):
        form = YouTubeDownloadForm(self.res_list, data={'select_format': 'Audio'})
        self.assertFalse(form.is_valid())

    def test_invalid_form_wrong_format(self):
        form = YouTubeDownloadForm(self.res_list, data={'select_format': 'XYZ', 'select_resolution': '1080p'})
        self.assertFalse(form.is_valid())

    def test_invalid_form_wrong_resolution(self):
        form = YouTubeDownloadForm(self.res_list, data={'select_format': 'Video', 'select_resolution': '100p'})
        self.assertFalse(form.is_valid())


# ------------ testing views.py --------------------
# def download(request):def settings(request):def home(request):

class TestHomeView(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('homepage')

    def test_homepage_GET(self):
        client = Client()

        response = client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class TestSettingsView(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.settings_url = reverse('settings')
        self.homepage_url = reverse('homepage')

    def test_settings_valid_post_GET(self):
        response = self.client.post(self.settings_url, {
            'youtube_url': "https://www.youtube.com/watch?v=znLbWOe4B6s"
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'download.html')

    def test_settings_empty_url_post_GET(self):
        response = self.client.post(self.settings_url, {
            'youtube_url': ""
        })

        self.assertEquals(response.status_code, 422)
        self.assertTemplateUsed(response, 'index.html')

    def test_settings_no_parameters_post_GET(self):
        response = self.client.post(self.settings_url, {
        })

        self.assertEquals(response.status_code, 422)
        self.assertTemplateUsed(response, 'index.html')

    def test_settings_response(self):
        data = {'youtube_url': "https://www.youtube.com/watch?v=znLbWOe4B6s"}
        response = self.client.post(self.settings_url, data=data)
        self.assertIn('form', response.context)
        self.assertIn('resolution_list', response.context)
        self.assertIn('url', response.context)

    def test_settings_resolution_list_component(self):
        data = {'youtube_url': "https://www.youtube.com/watch?v=jNQXAC9IVRw"}
        proper_resolutions = [('144p', '144p'), ('240p', '240p'), ('360p', '360p')]

        response = self.client.post(self.settings_url, data=data)
        self.assertEquals(proper_resolutions, response.context['resolution_list'])


class TestDownloadView(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.download_url = reverse('download')
        self.settings_url = reverse('settings')

    def test_download_mp4(self):
        data = {
            'url': "https://www.youtube.com/watch?v=jNQXAC9IVRw",
            "select_format": "Video",
            "select_resolution": "144p"
        }
        request = self.factory.post(self.download_url, data=data)
        response = download(request, data['url'])

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response.get('Content-Disposition'),
            "attachment; filename=Me at the zoo.mp4"
        )

    def test_download_mp3(self):
        data = {
            'url': "https://www.youtube.com/watch?v=jNQXAC9IVRw",
            "select_format": "Audio",
            "select_resolution": "144p"
        }
        request = self.factory.post(self.download_url, data=data)
        response = download(request, data['url'])

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response.get('Content-Disposition'),
            "attachment; filename=Me at the zoo.mp3"
        )

    def test_download_mp3_zip(self):
        data = {
            'url': "https://www.youtube.com/watch?v=jNQXAC9IVRw",
            "select_format": "Audio",
            "select_resolution": "144p",
            'select_metadata': 'on'
        }
        request = self.factory.post(self.download_url, data=data)
        response = download(request, data['url'])

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response.get('Content-Disposition'),
            "attachment; filename=content.zip"
        )

    def test_download_mp4_zip(self):
        data = {
            'url': "https://www.youtube.com/watch?v=jNQXAC9IVRw",
            "select_format": "Audio",
            "select_resolution": "144p",
            'select_metadata': 'on'
        }
        request = self.factory.post(self.download_url, data=data)
        response = download(request, data['url'])

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response.get('Content-Disposition'),
            "attachment; filename=content.zip"
        )


# class TestWholeFlow(LiveServerTestCase):
#
#     def test_homepage(self):
#         options = Options()
#         options.add_experimental_option("prefs", {
#             "download.default_directory": os.path.expanduser('~'),
#             "download.prompt_for_download": False,
#             "download.directory_upgrade": True,
#             "safebrowsing.enabled": True
#         })
#
#         driver = webdriver.Chrome(chrome_options=options)
#         driver.get('http://localhost:8000/')
#
#         assert "Home" in driver.title
#
#         home_yt_input = driver.find_element_by_id("id_youtube_url")
#         home_submit = driver.find_element_by_id("id_button_submit")
#
#         home_yt_input.send_keys("https://www.youtube.com/watch?v=jNQXAC9IVRw")
#         home_submit.click()
#
#         assert "Download the video" in driver.title
#
#         dl_form = driver.find_element_by_id("id_download_form")
#         dl_button = driver.find_element_by_id("id_download_button")
#
#         dl_button.click()
#
#         time.sleep(10)
#
#         assert os.path.exists(os.path.expanduser("~//Me at the zoo.mp4"))
#
#         os.remove(os.path.expanduser("~//Me at the zoo.mp4"))