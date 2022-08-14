from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from users import models as users_models

@login_required
def room(request, room_name):
    # extract user id values from the chat room name, there should be only 2 values
    users_list = room_name.split('and')
    # if the page is requested by someone other than the 2 users, return error
    if str(request.user.id) not in users_list:
        return HttpResponse("Unauthorized access")
    else:
        # iterate over user id values and extract the user instance for the other party
        for userid in users_list:
            # get the id which is different from that of the logged in user
            if int(userid) != request.user.id:
                try:
                    connection = users_models.AppUser.objects.get(id=int(userid))
                except users_models.AppUser.DoesNotExist:
                    return HttpResponse("Page not found", status=404)
        # define the values to be sent back when rendering
        context = {
            'room_name': room_name,
            'first_name': request.user.first_name,
            'connection': connection
        }
        return render(request, 'room.html', context)
        
