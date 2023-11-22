from app.ytdl import VideoInfo
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel


class Data(BaseModel):
    link: str


def link_gen(url):
    video = VideoInfo(url)
    first_url = video.get_best_video_url()

    if first_url:
        return first_url
    else:
        return 'No link found'


app = FastAPI()

formatted_data = {}

@app.get('/dl_link', status_code=status.HTTP_200_OK)
async def dl_link(data: Data):
    link = link_gen(data.link)
    formatted_data['Link'] = link

    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='link not found')
    return formatted_data
