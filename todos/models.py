
from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)  # fecha límite
    is_completed = models.BooleanField(default=False)   # resuelto o no
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title