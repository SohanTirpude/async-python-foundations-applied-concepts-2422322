import asyncio
import signal
import click
from contextlib import suppress
from websockets.asyncio.server import serve


async def blastoff(websocket):
    click.secho(">>  begin blastoff")
    for i in range(25):
        await websocket.send(f"\n\n\n>> {'  ' * i}🚀")
        await asyncio.sleep(0.03)
    for i in range(3):
        await asyncio.sleep(0.5)
        await websocket.send("\n\n\n>>   🚀🚀🚀🚀🚀🚀🚀🚀 BLASTOFF 🚀🚀🚀🚀🚀🚀🚀🚀  <<")


async def huston(websocket):
    click.clear()
    async for message in websocket:
        if "yes" in message.lower():
            click.secho(">> begin countdown")
            for i in reversed(range(1, 11)):
                await websocket.send(f"\n\n\n>>   Taking off in: {i}")
                await asyncio.sleep(0.8)
            with suppress(Exception):
                await blastoff(websocket)
        else:
            await websocket.send("Are you ready now?")


PORT = 8765


async def server():
    click.secho(f"--- listening for websocket connections on port: {PORT} ---")
    async with serve(huston, "localhost", PORT) as server:
        # Close the server when receiving SIGTERM.
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGTERM, server.close)
        await server.wait_closed()


asyncio.run(server())
