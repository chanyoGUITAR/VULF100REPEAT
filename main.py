from yt_dlp import YoutubeDL
import os
import json
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import * 
from moviepy.config import change_settings
from moviepy.video.fx.all import fadein, fadeout
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.0-Q16-HDRI\magick.exe"})

ydl_opts = {
    'format': 'best',
        # "postprocessors": [
        # {
        #     "key": "FFmpegExtractAudio",
        #     "preferredcodec": "m4a",
        # }]
            }

def mainpy(key, cout, dur, song_name, str_name, begin_sec):

    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.download(["https://www.youtube.com/watch?v="+key])

    for filename in os.listdir("./"):
        if key in filename:
            mp4name = filename

    clip = VideoFileClip(mp4name)

    str_main = " repeat " + str(cout) + " times"

    end_sec = begin_sec + dur

    # 動画を切り取る
    clip_cut = clip.subclip(begin_sec, end_sec)
    clip_cut_beg = clip.subclip(begin_sec-1, begin_sec)
    clip_cut_end = clip.subclip(end_sec, end_sec+4)

    clip_cut_buf = clip_cut

    txt_clip  = TextClip(str(cout), fontsize=100, color='white', 
                        bg_color='transparent', 
                        size=(500,500)).set_position(('center', 'center')).set_duration(dur)

    clip_cut_buf_addnum = CompositeVideoClip([clip_cut_buf, 
                                            txt_clip
                                            ])

    clip_cut = concatenate_videoclips([clip_cut_beg,clip_cut_buf_addnum])

    for i in range(cout-2,-2,-1):
        txt_clip  = TextClip(str(i+1)
                            , fontsize=150, color='white', 
                            bg_color='transparent', 
                            size=(500,500)).set_position(('center', 'center')).set_duration(dur)

        clip_cut_buf_addnum = CompositeVideoClip([clip_cut_buf, 
                                                txt_clip
                                                ])
        clip_cut = concatenate_videoclips([clip_cut,clip_cut_buf_addnum])

    clip_cut = concatenate_videoclips([clip_cut,clip_cut_end])
    clip_cut = fadein(fadeout(clip_cut,2),1).audio_fadeout(2).audio_fadein(1)

    clip_cut.write_videofile(song_name + str_name + str_main + ".mp4")


if __name__ == '__main__':

    with open('./input/input.json') as f:
        input = json.load(f)

    d = 1 # json num
    cout = 100 

    key = input[str(d)]["key"]
    dur = input[str(d)]["dur"]
    song_name = "VULFPECK " + input[str(d)]["song_name"] + " - "
    str_name = input[str(d)]["str_name"]
    begin_sec = input[str(d)]["begin_sec"]

    mainpy(key, cout, dur, song_name, str_name, begin_sec)
