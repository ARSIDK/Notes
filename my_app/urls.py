from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.create_note, name='create_note'),
    path('notes/', views.notes_list, name='notes_list'),
]

