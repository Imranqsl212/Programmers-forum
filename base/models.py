from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(null=True, blank=True)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # if user deleted it deletes all child
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # if chat deleted, message deleted
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        if len(self.body) >= 30:
            return self.body[0:30] + ' ...'
        else:
            return self.body
