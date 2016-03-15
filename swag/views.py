import youtube_dl, os, mutagen.id3, mutagen

from django.shortcuts import render
from django.views.generic import View
from .forms import YTForm
from django.conf import settings
from mutagen.easyid3 import EasyID3
from swag.models import DownloadedSongs

def index(request):
    return render(request, 'swag/index.html')

class YoutubeView(View):
    template_name = "swag/youtube.html"
    form_class = YTForm
    success_url = '/youtube'

    def get(self, request, *args, **kwargs):
        print ("GET: ", request.GET)
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        print ("POST: ", request.POST)
        form = self.form_class(request.POST)
        if form.is_valid():
            print (form.cleaned_data)
            ydl_opts = {
                'outtmpl': os.path.join(settings.MP3_FILE_TMP, "%(title)s.%(ext)s"),
                'format': 'bestaudio/best',
                'noplaylist': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192'
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                datas = ydl.extract_info(form.cleaned_data['url'])
            download_file = self.add_file_infos(os.path.join(settings.PROJECT_PATH, settings.MP3_FILE_TMP, datas['title'] + ".mp3"), datas, form.cleaned_data)
            test = DownloadedSongs(url=form.cleaned_data['url'])
            test.save()
            return render(request, self.template_name, {'form': form, 'file': download_file})
            return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})

    def add_file_infos(self, path, yt_datas, user_datas):
        """
        Edit the mp3 file (filename) metadatas
        return the full path
        """
        filename = yt_datas['title']
        datas = filename.split(' - ')
        try:
            file = EasyID3(path)
        except mutagen.id3.ID3NoHeaderError:
            file = mutagen.File(path, easy=True)
            file.add_tags()
        newdatas = {
            "title": user_datas['title'] or [(datas[2] if len(datas) > 2 else datas[1])],
            "artist": user_datas['artist'] or [(datas[1] if len(datas) > 2 else datas[0])]
        }
        for k in newdatas.keys():
            file[k] = newdatas[k]
        print (file)
        file.save()
        # newpath = os.path.join(os.path.dirname(path), datas['title'][0] + ".mp3")
        # os.rename(path, newpath)
        if settings.DEBUG == True:
            return ("swag/" + filename + ".mp3")
        else:
            return (filename + ".mp3")