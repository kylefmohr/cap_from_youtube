import time
from dataclasses import dataclass
import yt_dlp
import numpy as np
import cv2


@dataclass
class VideoStream:
    url: str = None
    resolution: str = None
    height: int = 0
    width: int = 0

    def __init__(self, video_format):
        self.url = video_format['url']
        self.height = video_format['height']
        self.width = video_format['width']
        self.frame_rate = video_format['fps']
        self.resolution = f'{self.height}p{self.frame_rate}'

    def __str__(self):
        return f'({self.height}x{self.width}): {self.url}'


def list_video_streams(url):
    cap = None

    # ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        streams = [VideoStream(format)
                   for format in info['formats'][::-1]
                   if format['vcodec'] != 'none']
        # Get the unique resolutions
        print(len(streams))
        resolutions = [stream.resolution for stream in streams if stream.resolution is not None]
        _, unique_indices = np.unique(np.array(resolutions), return_index=True)
        # _, unique_indices = np.unique(np.array([stream.resolution
        #                                         for stream in streams]), return_index=True)

        # Sort the streams by resolution, highest to lowest
        streams = [streams[index] for index in np.sort(unique_indices)]

        # Reverse the arrays to start with the highest resolution
        resolutions = np.array([stream.resolution for stream in streams])
        resolutions = resolutions[::-1]
        streams = streams[::-1]
        return streams, resolutions


def cap_from_youtube(url, resolution=None):
    streams, resolutions = list_video_streams(url)

    if not resolution or resolution == 'best':
        return cv2.VideoCapture(streams[-1].url)

    if resolution not in resolutions:
        raise ValueError(f'Resolution {resolution} not available')
    res_index = np.where(resolutions == resolution)[0][0]
    return cv2.VideoCapture(streams[res_index].url)


if __name__ == '__main__':

    from cap_from_youtube import list_video_streams

    youtube_url = 'https://youtu.be/LXb3EKWsInQ'
    streams, resolutions = list_video_streams(youtube_url)

    for stream in streams:
        print(stream)
