from django.contrib import admin
from .models import Note
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display=("title","updated_at","created_at")
    search_fields=("title","content")
    ordering=("-updated_at",)
