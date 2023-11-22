import json
from urllib.parse import urlunparse
from app.scraper import FacebookScraper as fb

import yt_dlp


class VideoInfo:
    def __init__(self, url):
        self.url = url
        self.ydl_opts = {
            'list_thumbnails': True,
            'listformats': True,
        }

    def preprocess_url(self):
        # If the URL doesn't start with http:// or https://, add http://
        if not self.url.startswith("http://") and not self.url.startswith("https://"):
            self.url = "http://" + self.url

        # If the URL doesn't have www. prefix, add it
        from urllib.parse import urlparse
        parsed_url = urlparse(self.url)
        if not parsed_url.netloc.startswith("www."):
            netloc = "www." + parsed_url.netloc
            self.url = urlunparse(
                (parsed_url.scheme, netloc, parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment))
        return self.url

    def get_video_info(self):

        link = self.preprocess_url()

        if 'facebook.com' in link:
            return fb(link).extract_fb_link()
        else:
            # Using yt_dlp (YouTube Downloader) to extract video information
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(link, download=False)
                if "formats" in info:
                    video_formats = info["formats"]
                    # Check if there are available video formats
                    if video_formats:
                        video = video_formats[-1]['url']
                        return video
                return None

    def get_best_video_url(self):

        link = self.get_video_info()
        return link


