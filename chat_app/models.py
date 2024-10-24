from django.db import models
from django.contrib.auth.models import User

class Channel(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='channels')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    channel = models.ForeignKey(Channel, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username}: {self.content[:20]}'

