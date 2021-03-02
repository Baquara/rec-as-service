from flask import Flask, render_template, request, jsonify
import re
import json
import requests
import uuid
import json
from youtube_search import YoutubeSearch
from bs4 import BeautifulSoup
import youtube_dl
from pydeezer import Deezer
from pydeezer import Downloader
from pydeezer.constants import track_formats

arl = "2b31f62ab60ea6e5486f95405be1f2647d6ce3257a9940f3f5a9a2b1a66f0ba6718007f55cbb14c2821927053000918f320a51160665b6813dbf37b7151d924b569127085d80c80deeb521200a55598bbf242ecdce8eecfe404d4404b49ff70f"
deezer = Deezer(arl=arl)
user_info = deezer.user
download_dir = "/home/baquara/Música/"

app = Flask(__name__)
my_id = uuid.uuid1()

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}

ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist':'True',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3'
    }],
}



def download(textarea,url):
    return 0
    try:
        track_search_results = deezer.search_tracks(textarea)
        track = deezer.get_track(track_search_results[0]['id'])
    except:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        raise Exception('The song could not be downloaded on Deezer')
    while True:
        try:
            track["download"](download_dir, quality=track_formats.MP3_320)
            break
        except:
            pass


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/returnebd", methods=['POST'])
def returnebd():
    textarea = request.json.get("textarea", None)
    soup = BeautifulSoup(textarea,features="lxml")
    textarea= soup.get_text()
    finalstring=""
    try: 
        results = YoutubeSearch(textarea, max_results=1).to_json()
        results = json.loads(results)
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            video = ydl.extract_info('http://youtube.com/watch?v='+results["videos"][0]["id"], download=False)
        yt = video["url"]
        try:
            finalstring=finalstring+'''<div>'''+(video["artist"]+" - "+video["track"])+'''</div><audio controls><source src="'''+yt+'''"></audio>'''
            try:
                download(textarea,'http://youtube.com/watch?v='+results["videos"][0]["id"])
            except Exception as e:
                finalstring = finalstring+"<div>Error: "+str(e)+" | SONG "+textarea+" COULD NOT BE DOWNLOADED.</div>"
        except Exception as e:
            print("An error occured !!! "+str(e))
            finalstring=finalstring+'''<div>'''+results["videos"][0]["title"]+'''</div><audio  controls><source src="'''+yt+'''"></audio>'''
            try:
                download(textarea,'http://youtube.com/watch?v='+results["videos"][0]["id"])
            except Exception as e:
                finalstring = finalstring+"<div>Error: "+str(e)+" | SONG "+textarea+" COULD NOT BE DOWNLOADED.</div>"
    except Exception as e:
        print(e)
        finalstring = "<div>Error: "+str(e)+" | SONG "+textarea+" COULD NOT FOUND OR BE DOWNLOADED.</div>"
        pass
    return finalstring

if __name__ == "__main__":
    app.run()
 
