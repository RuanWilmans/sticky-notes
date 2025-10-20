from django.test import TestCase
from django.urls import reverse, resolve
from .models import Note
from .forms import NoteForm
from . import views


class NoteModelTests(TestCase):
    def test_create_note_and_str(self):
        n = Note.objects.create(title="Groceries", content="Eggs, milk")
        self.assertTrue(n.pk)
        self.assertEqual(str(n), "Groceries")


class NoteFormTests(TestCase):
    def test_form_valid(self):
        form = NoteForm(data={"title": "Valid", "content": "Body"})
        self.assertTrue(form.is_valid())

    def test_form_invalid_when_title_missing(self):
        form = NoteForm(data={"title": "", "content": "Body"})
        self.assertFalse(form.is_valid())


class NoteURLTests(TestCase):
    def test_url_routes(self):
        self.assertEqual(resolve("/").func, views.note_list)
        self.assertEqual(resolve("/new/").func, views.note_create)


class NoteViewTests(TestCase):
    def setUp(self):
        self.note = Note.objects.create(title="Init", content="Seed")

    def test_list_view_renders(self):
        r = self.client.get(reverse("note_list"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Init")
        self.assertTemplateUsed(r, "notes/note_list.html")

    def test_create_view_get(self):
        r = self.client.get(reverse("note_create"))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, "notes/note_form.html")

    def test_create_view_post_valid(self):
        r = self.client.post(reverse("note_create"), {"title": "New", "content": "Body"})
        self.assertEqual(r.status_code, 302)  # redirect
        self.assertTrue(Note.objects.filter(title="New").exists())

    def test_update_view_post(self):
        url = reverse("note_update", args=[self.note.pk])
        r = self.client.post(url, {"title": "Changed", "content": "Body"})
        self.assertEqual(r.status_code, 302)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Changed")

    def test_delete_view_post(self):
        url = reverse("note_delete", args=[self.note.pk])
        r = self.client.post(url)
        self.assertEqual(r.status_code, 302)
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())
