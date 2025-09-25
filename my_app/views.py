from django.shortcuts import render, redirect, get_object_or_404
from .forms import NoteForm
from .models import Note
# Create your views here.
# def index(request):
#     return render(request, 'index.html')

# def goodbye(request):
#     return render(request, 'goodbye.html')

def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notes_list')  
    else:
        form = NoteForm()
    
    return render(request, 'notes/note_form.html', {'form': form})


def delete_note(request, pk):  
    note = get_object_or_404(Note, id=pk)
    
    if request.method == 'POST':
        note.delete()
        return redirect('notes:notes_list')


def notes_list(request):
    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'notes/notes_list.html', {'notes': notes})