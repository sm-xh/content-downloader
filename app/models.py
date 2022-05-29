from django.db import models

# Create your models here.


class YouTubeDownloader(models.Model):
    youtube_url = models.CharField(max_length=43)

    def __str__(self):
        return self.youtube_url
