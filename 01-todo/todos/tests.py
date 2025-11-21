from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Todo


class TodoViewsTests(TestCase):
    def setUp(self):
        self.todo1 = Todo.objects.create(
            title="Z tarea",
            description="desc",
            due_date=timezone.now().date(),
            is_completed=False,
        )
        self.todo2 = Todo.objects.create(
            title="A tarea",
            description="desc",
            due_date=timezone.now().date(),
            is_completed=True,
        )

    def test_todo_list_uses_template_and_orders(self):
        response = self.client.get(reverse("todo_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todos/home.html")
        todos = list(response.context["todos"])
        self.assertEqual(todos[0], self.todo1)
        self.assertEqual(todos[1], self.todo2)

    def test_todo_create_valid_post(self):
        data = {
            "title": "Nueva",
            "description": "desc",
            "due_date": timezone.now().date(),
            "is_completed": False,
        }
        response = self.client.post(reverse("todo_create"), data)
        self.assertRedirects(response, reverse("todo_list"))
        self.assertEqual(Todo.objects.count(), 3)

    def test_todo_update(self):
        data = {
            "title": "Actualizada",
            "description": "desc",
            "due_date": timezone.now().date(),
            "is_completed": True,
        }
        response = self.client.post(reverse("todo_update", args=[self.todo1.pk]), data)
        self.assertRedirects(response, reverse("todo_list"))
        self.todo1.refresh_from_db()
        self.assertEqual(self.todo1.title, "Actualizada")
        self.assertTrue(self.todo1.is_completed)

    def test_todo_delete(self):
        response_get = self.client.get(reverse("todo_delete", args=[self.todo1.pk]))
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "todos/todo_confirm_delete.html")

        response_post = self.client.post(reverse("todo_delete", args=[self.todo1.pk]))
        self.assertRedirects(response_post, reverse("todo_list"))
        self.assertFalse(Todo.objects.filter(pk=self.todo1.pk).exists())

    def test_toggle_complete(self):
        response = self.client.post(reverse("todo_toggle_complete", args=[self.todo1.pk]))
        self.assertRedirects(response, reverse("todo_list"))
        self.todo1.refresh_from_db()
        self.assertTrue(self.todo1.is_completed)

    def test_create_invalid_form_rerenders(self):
        response = self.client.post(reverse("todo_create"), {"description": "desc"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todos/todo_form.html")
        self.assertEqual(Todo.objects.count(), 2)
