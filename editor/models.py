from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255, default="Untitled Document")
    content = models.TextField(blank=True)  
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title