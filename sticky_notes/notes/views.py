from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm

def note_list(request):
    notes=Note.objects.order_by("-updated_at")
    return render(request,"notes/note_list.html",{"notes":notes,"page_title":"Sticky Notes"})

def note_create(request):
    if request.method=="POST":
        form=NoteForm(request.POST)
        if form.is_valid():
            form.save(); return redirect("note_list")
    else:
        form=NoteForm()
    return render(request,"notes/note_form.html",{"form":form,"mode":"Create"})

def note_update(request, pk:int):
    note=get_object_or_404(Note, pk=pk)
    if request.method=="POST":
        form=NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save(); return redirect("note_list")
    else:
        form=NoteForm(instance=note)
    return render(request,"notes/note_form.html",{"form":form,"mode":"Update"})

def note_delete(request, pk:int):
    note=get_object_or_404(Note, pk=pk)
    if request.method=="POST":
        note.delete(); return redirect("note_list")
    return render(request,"notes/note_confirm_delete.html",{"note":note})
