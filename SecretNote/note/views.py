from django.shortcuts import render,redirect
from django.http import Http404
from django.http import HttpResponse
from .models import Note
from .forms import CreateNote
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "note/home.html")

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
            note = form.save(commit=False)
            note.user = request.user 
            note.save()
            return redirect('/')
        
    else:
        form = CreateNote()
    return render(request, "note/create_note.html", {"form": form})

@login_required  
def user_notes(request):
    print(f"Current user: {request.user}")
    notes = Note.objects.filter(user=request.user) 
    print(f"Number of notes for user {request.user}: {notes.count()}")
    return render(request, 'note/user_notes.html', {'notes': notes})
 