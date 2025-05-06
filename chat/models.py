from uuid import uuid4

from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model


User = get_user_model()


class Chat(models.Model):
    name = models.CharField(max_length=32, default=uuid4)
    users_online = models.ManyToManyField(User, related_name='online_users', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __str__(self):
        return self.name
