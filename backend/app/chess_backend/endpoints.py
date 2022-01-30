from django.http.response import JsonResponse
from rest_framework.views import APIView
from .models import Game
import random, string
import json
from rest_framework.permissions import IsAuthenticated
import chess

# Create your views here.

class AcceptGameInvite(APIView):
    permission_classes=[IsAuthenticated,]
    def post(self, request, game_key):
        game = Game.objects.get(key=game_key)
        already_accepted = False
        if game.white is None:
            game.white = request.user
        elif(game.black is None):
            game.black = request.user
        else:
            already_accepted = True

        if(already_accepted):
            return JsonResponse(data={"error":"Both players already accepted invite"})
        else:
            game.save()
            return JsonResponse(data={"ok":"ok"})

class GameEndpoint(APIView):
    permission_classes=[IsAuthenticated,]
    def get(self, request, game_key):
        game = Game.objects.get(key=game_key)

        history = [move.move_from+move.move_to for move in game.moves.all()]

        accepted = (game.white == request.user or game.black == request.user)
        both_players_ready = not (game.white is None or game.black is None)
        
        if(game.white == request.user):
            playing = "white"
        elif(game.black == request.user):
            playing = "black"
        else:
            playing = None

        if(game.is_over):
            if(game.winner):
                if(game.winner == game.white):
                    result = "1-0"
                else:
                    result = "0-1"
            else:
                result = "1/2-1/2"
        else:
            result = None

        return JsonResponse(data={
            "fen":game.fen, 
            "history": history, 
            "accepted": accepted, 
            "both_players_ready": both_players_ready,
            "white": game.white.username if game.white else "",
            "black": game.black.username if game.black else "",
            "playing": playing,
            "result": result
            })


    def post(self, request):
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        creator_color = random.randint(0,1)
        if(creator_color == 1):
            white = request.user
            black = None
        else:
            white = None
            black = request.user

        game = Game.objects.create(
            key=key,
            fen = chess.STARTING_FEN,
            white = white,
            black = black
        )

        return JsonResponse(data={"game_key": key, "white": creator_color})
