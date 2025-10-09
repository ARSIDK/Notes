from django.urls import path
from . import views
from django.urls import path
from .views import NoteListView, NoteCreateView, NoteUpdateView, NoteDeleteView, NoteDetailView


urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.create_note, name='create_note'),
    path('', NoteListView.as_view(), name='notes_list'),
    path('notes/', views.notes_list, name='notes_list'),
    path('create/', NoteCreateView.as_view(), name='note_create'),
    path('<int:pk>/', NoteDetailView.as_view(), name='note_detail'),
    path('<int:pk>/edit/', NoteUpdateView.as_view(), name='note_edit'),
    path('<int:pk>/delete/', NoteDeleteView.as_view(), name='note_delete'),
    
]