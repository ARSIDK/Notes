from django import forms
from .models import Note
from django.utils import timezone

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'due_date', 'tags', 'is_completed']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Введите заголовок заметки',
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Начните писать вашу заметку здесь...',
                'rows': 15,
                'class': 'form-control'
            }),
            'due_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'is_completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['due_date'].initial = timezone.now().strftime('%Y-%m-%dT%H:%M')
        
          






