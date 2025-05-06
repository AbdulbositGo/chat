from django.shortcuts import render

# Create your views here.


def chat(request):
    return render(request, 'chat/chats.html', {'user_messages': range(10)})
