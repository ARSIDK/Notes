from django.db import models

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


    
class Tag(models.Model):
    """Модель для тегов заметок"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")
   
    def __str__(self):
        return self.name
    
class Note(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]
    title = models.CharField("Заголовок", max_length=100)
    content = models.TextField("Содержание")
    created_at = models.DateTimeField("Дата создания", default=timezone.now)
    due_date = models.DateTimeField("Срок выполнения", blank=True, null=True)
    tags = models.CharField("Теги", max_length=100, blank=True)
    is_completed = models.BooleanField("Выполнено", default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name='notes')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    pinned = models.BooleanField(default=False, verbose_name="Закреплена")
 
    priority = models.CharField('Приоритет', max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ['-pinned', '-created_at']
        
    def __str__(self):
        return self.title
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")
   
def __str__(self):
        return self.title or f"Заметка #{self.id}"

def get_absolute_url(self):
        return reverse('note-detail', kwargs={'pk': self.pk})


def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',')] if self.tags else []

    
    