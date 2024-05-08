from django import forms

class AudioUploadForm(forms.Form):
    audio = forms.FileField(widget=forms.FileInput(attrs={'class':'audio_control'}))


