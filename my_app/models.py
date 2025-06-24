from django.db import models

# Create your models here.

from django.utils import timezone

class Note(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    content = models.TextField("Содержание")
    created_at = models.DateTimeField("Дата создания", default=timezone.now)
    due_date = models.DateTimeField("Срок выполнения", blank=True, null=True)
    tags = models.CharField("Теги", max_length=100, blank=True)
    is_completed = models.BooleanField("Выполнено", default=False)

    def __str__(self):
        return self.title