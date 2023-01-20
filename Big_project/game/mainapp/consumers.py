import json
import redis

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    # redis instance
    redis_client = redis.StrictRedis.from_url("rediss://red-cegkhc02i3mkhvoakgh0:Z6M9PSoaNV0aOv0XR2y3CmJ8TpYGGGfQ@singapore-redis.render.com:6379/5", encoding="utf-8", decode_responses=True)

    def connect(self):
        # routing.py 참조
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.player_name = self.scope["url_route"]["kwargs"]["player_name"]
        self.room_group_name = "chat_%s" % self.room_name

        print(self.room_name, self.player_name)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        
        ### redis
        self.score_group_name = "score_%s" % self.room_name
        # (set_id, score, player_name)
        self.redis_client.zadd(self.score_group_name, {self.player_name: 0})


        ### publish to other players
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "enter", "message": {}}
        )


    def disconnect(self, close_code):
        # Leave room group
        self.redis_client.zrem(self.score_group_name, self.player_name)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    # 본인으로부터 메시지 받으면
    def receive(self, text_data):
        print('recived')

        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        message_type = text_data_json["type"]

        # Send message to room group
        if message_type == "enter":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "enter", "message": message}
            )
        elif message_type == "attack":
            # score update in redis
            self.redis_client.zincrby(self.score_group_name, 10.0, self.player_name)
            # 공격했다고 모두에게 알림
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "attack", "message": message}
            )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

    def enter(self, event):
        message = event["message"]
        message_type = event["type"]
        # 스코어보드 업데이트 요청
        score_board = self.redis_client.zrange(self.score_group_name, 0, -1, desc=True, withscores=True)
        # Send message to WebSocket
        self.send(text_data=json.dumps({"type": message_type, "message": score_board}))

    def attack(self, event):
        message = event["message"]
        message_type = event["type"]
        # 스코어보드 업데이트 요청
        score_board = self.redis_client.zrange(self.score_group_name, 0, -1, desc=True, withscores=True)
        # Send message to WebSocket
        self.send(text_data=json.dumps({"type": message_type, "message": score_board}))


class WaitRoomConsumer(WebsocketConsumer):
    # redis instance
    redis_client = redis.StrictRedis.from_url("rediss://red-cegkhc02i3mkhvoakgh0:Z6M9PSoaNV0aOv0XR2y3CmJ8TpYGGGfQ@singapore-redis.render.com:6379/10", encoding="utf-8", decode_responses=True)

    def connect(self):
        # routing.py 참조
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.player_name = self.scope["url_route"]["kwargs"]["player_name"]
        self.room_group_name = "wait_room_%s" % self.room_name

        print(self.room_name, self.player_name)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        
        ### publish to other players
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "enter_wait_room", "message": self.player_name}
        )

        ### redis
        self.redis_client.sadd(self.room_name, self.player_name)
        players_in_room =  list(self.redis_client.smembers(self.room_name))
        print(players_in_room)
        self.send(text_data=json.dumps({"type": "i_entered", "message": players_in_room}))

    def disconnect(self, close_code):
        # Leave room group
        # self.redis_client.zrem(self.score_group_name, self.player_name)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        self.redis_client.srem(self.room_name, self.player_name)
        ### publish to other players
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "leave", "message": self.player_name}
        )


    # Receive message from WebSocket
    # 본인으로부터 메시지 받으면
    def receive(self, text_data):
        print('recived')

        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        message_type = text_data_json["type"]


    def enter_wait_room(self, event):
        message = event["message"]
        message_type = event["type"]
        # Send message to WebSocket
        # 본인이 보낸 게 아닐 때만
        if message != self.player_name:
            self.send(text_data=json.dumps({"type": message_type, "message": message}))


    def leave(self, event):
        message = event["message"]
        message_type = event["type"]
        # Send message to WebSocket
        # 제거된 player만 넘김
        self.send(text_data=json.dumps({"type": message_type, "message": message}))