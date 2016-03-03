import youtube_dl

from django.shortcuts import render
from django.views.generic import View
from .forms import YTForm

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
            print ("Woohoo c valid")
            ydl_opts = {
                'outtmpl': 'swag/static/swag/kaka.%(ext)s',
                'format': 'bestaudio/best',
                'noplaylist': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([form.cleaned_data['url']])
            download_file = "static/swag/kaka.mp3"
            return render(request, self.template_name, {'form': form, 'file': download_file})
        return render(request, self.template_name, {'form': form})
