from django import forms
from .models import Note

class CreateNote(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'expiration', 'max_views']


