from django.shortcuts import render,redirect
from django.http import Http404
from django.http import HttpResponse
from .models import Note
from .forms import CreateNote
from django.contrib.auth.forms import UserCreationForm


def view_note(request,id):
    try:
        note = Note.objects.get(url_id=id)
    except Note.DoesNotExist:
        raise Http404("This note doesn't exist")
    return HttpResponse(note)

def create_note(request):
    if request.method == "POST":
        form = CreateNote(request.POST)
        if form.is_valid():
            note = form.save()
            note.user = request.user 
            note.save()
            print('valid create note request')
            return redirect('/')
        else: 
            print('invalid create note request')
        
    else:
        form = CreateNote()


    return render(request, "note/create_note.html", {"form": form})

 