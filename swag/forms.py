from django import forms

class YTForm(forms.Form):
    url = forms.URLField(label="URL")
    artist = forms.CharField(required=False, label="Artist")
    title = forms.CharField(required=False, label="Title")
    album = forms.CharField(required=False, label="Album")
    genre = forms.MultipleChoiceField(required=False, label="Genres", choices=(
        ('HC', 'Hardcore'),
        ('FC', 'Frenchcore'),
        ('DNB', "Drum'n'Bass"),
        ('RT', "Raggatek")
    ))
