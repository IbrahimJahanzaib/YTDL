import json
import yt_dlp

class TikTokVideoInfo:
    def __init__(self, url):
        self.url = url
        self.ydl_opts = {}
    
    def get_video_info(self):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(self.url, download=False)
            return info

    def get_best_video_url(self):
        info = self.get_video_info()
        
        if 'formats' in info:
            video_formats = info['formats']
            if video_formats:
                return video_formats
        return None

# first_format = video_formats[0]
# return first_format['url']


