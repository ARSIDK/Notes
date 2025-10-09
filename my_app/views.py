from django.shortcuts import render, redirect, get_object_or_404
from .forms import NoteForm
from .models import Note
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

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
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'
    
    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('notes_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('notes_list')
    
    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('notes_list')
    
    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'notes/note_detail.html'
    
    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)
    


