from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    title = models.CharField(max_length=255, default="Untitled Document")
    content = models.TextField(blank=True)  
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    start = models.IntegerField()  # Start index of the comment in the document
    end = models.IntegerField()    # End index of the comment in the document
    created_at = models.DateTimeField(auto_now_add=True)

