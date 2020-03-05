from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json
from .room_generator import RoomGenerator


# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))


@csrf_exempt
@api_view(["GET"])
def initialize(request):

    # set the user
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)
    print("REQUEST: ", request)
    return JsonResponse({'uuid': uuid, 'name': player.user.username, 'title': room.title, 'description': room.description, 'players': players}, safe=True)


@api_view(["GET"])
def rooms(request):
    print("RRRRRROOOOOOOOMMMMMMMMSSSSSSS!!!!!!!!!!!!!!")
    # create the rooms with the room_gen
    Room.objects.all().delete()
    generated_rooms = RoomGenerator()
    num_rooms = 101
    width = 10
    height = 10
    generated_rooms.generate_rooms(width, height, num_rooms)

    rooms = Room.objects.all()
    room_data = []
    for room in rooms:
        room_data.append(
            {"id": room.id, "title": room.title, "description": room.description, "north": room.n_to, "east": room.e_to, "south": room.s_to, "west": room.w_to, "x": room.x_c, "y": room.y_c})
    """ 
    w = World()
    num_rooms = 44
    width = 8
    height = 7
    w.generate_rooms(width, height, num_rooms)
    w.print_rooms()
    """
    # w = World()
    # num_rooms = 44
    # width = 8
    # height = 7
    # w.generate_rooms(width, height, num_rooms)
    # w.print_rooms()

    return JsonResponse({'num_rooms': len(room_data), 'rooms': room_data}, safe=True)


# @csrf_exempt
@api_view(["POST"])
def move(request):
    print("MOVE!!!!!!!")
    dirs = {"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()
    nextRoomID = None
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom = nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'name': player.user.username, 'title': nextRoom.title, 'description': nextRoom.description, 'players': players, 'error_msg': ""}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name': player.user.username, 'title': room.title, 'description': room.description, 'players': players, 'error_msg': "You cannot move that way."}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error': "Not yet implemented"}, safe=True, status=500)
