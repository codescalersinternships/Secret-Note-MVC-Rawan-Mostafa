from django import forms
from .models import Note
from django.core.exceptions import ValidationError
from django.utils import timezone

class CreateNote(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'expiration', 'max_views']

    def clean_expiration(self):
        expiration = self.cleaned_data.get('expiration')
        if expiration < timezone.now():
            raise ValidationError("Expiration date cant be in the past", code="invalid")
        return expiration



