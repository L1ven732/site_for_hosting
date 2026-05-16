from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Expression_result(models.Model):
    expression = models.TextField()

class StringAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    input_text = models.TextField()
    word_count = models.PositiveIntegerField()
    char_count = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.input_text[:30]}... ({self.timestamp})"