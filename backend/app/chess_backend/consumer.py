import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from chess_backend.models import Game, Move, Bet
import chess

class GameConsumer(WebsocketConsumer):
    def connect(self):
        if not self.scope["user"].is_anonymous:
            self.game_key = self.scope['url_route']['kwargs']['game_key']
            self.game_group_name = self.game_key
            

            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.game_group_name,
                self.channel_name
            )

            self.accept()

            async_to_sync(self.channel_layer.group_send)(
                    self.game_group_name,
                    {
                        'type': 'send_ready'
                    }
                )

            

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name,
            self.channel_name
        )

    def send_ready(self, event):
        game = Game.objects.get(key=self.game_key)

        if(not (game.white is None or game.black is None)):
            ready = "both"
        elif(game.white is None):
            ready = "black"
        elif(game.black is None):
            ready="white"
        else:
            ready=None

        self.send(text_data=json.dumps({
            "ready":ready
            }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if("move" in text_data_json):
            game = Game.objects.get(key=self.game_key)
            move_from = text_data_json["move"]['from']
            move_to = text_data_json["move"]['to']

            board = chess.Board(chess.STARTING_FEN)
            for move in game.moves.all():
                board.push_uci(move.move_from + move.move_to)

            move = chess.Move.from_uci(move_from+move_to)

            if board.turn == chess.WHITE:
                player_to_move = game.white
            else:
                player_to_move = game.black
            if move in board.legal_moves and self.scope["user"] == player_to_move:
                board.push_uci(move_from+move_to)

                outcome = board.outcome()

                

                move = Move.objects.create(
                    move_from = move_from,
                    move_to = move_to,
                    made_by = self.scope["user"],
                )

                game.moves.add(move)
                game.fen = board.fen()

                if outcome is not None:
                    result = outcome.result()
                    if(result == "1-0"):
                        #WHITE WIN
                        game.winner = game.white
                    elif(result == "0-1"):
                        #BLACK WIN
                        game.winner = game.black
                    game.is_over = True
                else:
                    result = None

                async_to_sync(self.channel_layer.group_send)(
                    self.game_group_name,
                    {
                        'type': 'chess_move',
                        'from': text_data_json["move"]['from'],
                        'to': text_data_json["move"]['to'],
                        'result': result
                    }
                )

                game.save()
                
            else:
                #illegal move sent, bad client
                pass
        elif("bet" in text_data_json):
            async_to_sync(self.channel_layer.group_send)(
                self.game_group_name,
                {
                    'type': 'bet',
                    'amount': text_data_json["bet"]['amount'],
                    'action': text_data_json["bet"]['action']
                }
            )
        

    def chess_move(self, event):
        move_from = event['from']
        move_to = event['to']
        result = event['result']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'move':{
                'from': move_from,
                'to': move_to,
                'result': result
            }
        }))


    def bet(self, event):
        action = event['action']
        amount = event['amount']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'bet':{
                'action': action,
                'amount': amount,
            }
        }))