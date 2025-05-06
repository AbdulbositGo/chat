from django.shortcuts import render

from .models import Chat, Message

# Create your views here.


def chat(request):
    messages = Chat.objects.first().message_set.all()
    return render(request, 'chat/chats.html', {'user_messages': messages})
