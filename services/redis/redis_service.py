import json

import redis
import pickle


class RedisService:
    def __init__(self):
        self.redis_client = redis.Redis(host="redis", port=6379, db=0)

    def set_chat(self, chat_id, chat_messages):
        self.redis_client.set(chat_id, pickle.dumps(chat_messages))
        self.redis_client.expire(chat_id, 1800, nx=True)

    def get_chat(self, chat_id):
        return self.redis_client.get(chat_id)

    def delete_chat(self, chat_id):
        self.redis_client.delete(chat_id)

    def get_personas(self, set_name='persona'):
        return [json.loads(element) for element in self.redis_client.lrange(set_name, 0, -1)]

    def add_persona(self, key, value, set_name='persona'):
        self.delete_persona(key)
        self.redis_client.rpush(set_name, json.dumps(value))

    def delete_persona(self, key, set_name='persona'):
        objects = [json.loads(element) for element in self.redis_client.lrange(set_name, 0, -1)]
        for i in range(len(objects)):
            item = objects[i]
            if item['id'] == key:
                self.redis_client.lset(set_name, i, '_DELETE_')
                self.redis_client.lrem(set_name, 1, '_DELETE_')
