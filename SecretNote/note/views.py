from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from .models import Note

def view_note(request,id):
    try:
        note = Note.objects.get(url_id=id)
    except Note.DoesNotExist:
        raise Http404("This note doesn't exist")
    return HttpResponse(note)

 