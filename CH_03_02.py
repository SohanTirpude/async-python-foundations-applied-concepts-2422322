import asyncio
from redis import asyncio as aioredis
import click
import json


class Chat:
    def __init__(self, room_name):
        self.room_name = room_name

    async def start_db(self):
        pool = aioredis.ConnectionPool.from_url("redis://localhost")
        self.redis = aioredis.Redis.from_pool(pool)
        await self.redis.set("room_name", self.room_name)

    async def save_message(self, message_dictionary):
        room_name = await self.redis.get("room_name")
        message_json = json.dumps(message_dictionary)
        await self.redis.rpush(room_name, message_json)

    async def clear_db(self):
        await self.redis.flushall()

    async def get_all_messages(self):
        room_name = await self.redis.get("room_name")
        message_jsons = await self.redis.lrange(room_name, 0, -1)
        messages = []
        for message in message_jsons:
            message_dictionary = json.loads(message)
            messages.append(message_dictionary)
        return messages


async def main():
    chat_db = Chat("messages")
    await chat_db.start_db()
    await chat_db.save_message({"handle": "first_user", "message": "hey"})
    await chat_db.save_message({"handle": "first_user", "message": "hey"})
    await chat_db.save_message({"handle": "second_user", "message": "What's up?"})
    await chat_db.save_message({"handle": "first_user", "message": "all good!"})

    chat_messages = await chat_db.get_all_messages()

    click.secho(f" Chat ", fg="cyan", bold=True, bg="yellow")
    for message in chat_messages:
        click.secho(f'  {message["handle"]} | {message["message"]} ', fg="cyan")
    await chat_db.clear_db()

asyncio.run(main())
