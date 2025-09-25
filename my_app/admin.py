
# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.admin import DateFieldListFilter
from .models import Note, Tag

# Фильтр для статуса заметки
class StatusFilter(admin.SimpleListFilter):
    title = 'Статус заметки'
    parameter_name = 'status'
    
    def lookups(self, request, model_admin):
        return (
            ('active', 'Активные'),
            ('pinned', 'Закрепленные'),
            ('archived', 'В архиве'),
            ('empty', 'Без содержания'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(status='active')
        elif self.value() == 'pinned':
            return queryset.filter(pinned=True)
        elif self.value() == 'archived':
            return queryset.filter(status='archived')
        elif self.value() == 'empty':
            return queryset.filter(content__exact='') | queryset.filter(content__isnull=True)
        return queryset
    
class TagFilter(admin.SimpleListFilter):
    title = 'Теги'
    parameter_name = 'tag'
    
    def lookups(self, request, model_admin):
        return [(tag.id, tag.name) for tag in Tag.objects.all()]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tags__id=self.value())
        return queryset

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    
    list_display = [
        'colored_title_display',  # Переименовали метод
        'author', 
        'status_badge_display',   # Переименовали метод
        'tags_list_display',      # Переименовали метод
        'created_at_formatted',   # Переименовали метод
        'updated_at_formatted',   # Переименовали метод
        'content_preview_display' # Переименовали метод
    ]
    
    list_display_links = ['colored_title_display']
    
    search_fields = ['title', 'content', 'author__username', 'tags__name']
    
    list_filter = [
        StatusFilter,
        TagFilter,
        ('pinned', admin.BooleanFieldListFilter),  
        ('created_at', DateFieldListFilter),
        ('updated_at', DateFieldListFilter),
        ('author', admin.RelatedOnlyFieldListFilter),  
    ]
    
    date_hierarchy = 'created_at'
    list_per_page = 25
    filter_horizontal = ['tags']
    
    readonly_fields = ['created_at_formatted', 'updated_at_formatted']  # Используем методы
    
    actions = ['archive_notes', 'unarchive_notes', 'pin_notes', 'unpin_notes']
    
    def colored_title_display(self, obj):
        if obj.color and obj.color != "#ffffff":
            return format_html(
                '<span style="background-color: {}; padding: 2px 5px; border-radius: 3px; color: white;">{}</span>',
                obj.color,
                obj.title or f"Заметка #{obj.id}"
            )
        return obj.title or f"Заметка #{obj.id}"
    colored_title_display.short_description = 'Заголовок'
    
    def status_badge_display(self, obj):
        status_colors = {
            'active': 'green',
            'archived': 'gray',
            'deleted': 'red'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 10px; font-size: 12px;">{}</span>',
            status_colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge_display.short_description = 'Статус'
    
    def tags_list_display(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    tags_list_display.short_description = 'Теги'
    
    def created_at_formatted(self, obj):
        return obj.created_at.strftime("%d.%m.%Y %H:%M")
    created_at_formatted.short_description = 'Создана'
    
    def updated_at_formatted(self, obj):
        return obj.updated_at.strftime("%d.%m.%Y %H:%M")
    updated_at_formatted.short_description = 'Изменена'
    
    def content_preview_display(self, obj):
        if obj.content:
            preview = obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
            return format_html('<span title="{}">{}</span>', obj.content, preview)
        return "-"
    content_preview_display.short_description = 'Превью содержания'
    
    # Методы для readonly_fields
    def created_at_formatted(self, obj):
        return obj.created_at.strftime("%d.%m.%Y %H:%M")
    created_at_formatted.short_description = 'Создана'
    
    def updated_at_formatted(self, obj):
        return obj.updated_at.strftime("%d.%m.%Y %H:%M")
    updated_at_formatted.short_description = 'Изменена'
    
    def archive_notes(self, request, queryset):
        updated = queryset.update(status='archived')
        self.message_user(request, f"{updated} заметок перемещено в архив.")
    archive_notes.short_description = "Переместить в архив"
    
    def unarchive_notes(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, f"{updated} заметок восстановлено из архива.")
    unarchive_notes.short_description = "Восстановить из архива"
    
    def pin_notes(self, request, queryset):
        updated = queryset.update(pinned=True)
        self.message_user(request, f"{updated} заметок закреплено.")
    pin_notes.short_description = "Закрепить заметки"
    
    def unpin_notes(self, request, queryset):
        updated = queryset.update(pinned=False)
        self.message_user(request, f"{updated} заметок откреплено.")
    unpin_notes.short_description = "Открепить заметки"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'colored_tag_display', 'notes_count_display']
    search_fields = ['name']
    
    def colored_tag_display(self, obj):
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px;">{}</span>',
            obj.color,
            obj.name
        )
    colored_tag_display.short_description = 'Внешний вид'
    
    def notes_count_display(self, obj):
        return obj.note_set.count()
    notes_count_display.short_description = 'Кол-во заметок'