from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def room(request, room_name):
    context = {
        'room_name': room_name,
        'first_name': request.user.first_name
    }
    return render(request, 'room.html', context)
