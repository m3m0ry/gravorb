import asyncio
import aioconsole
import json

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, user):
        self.user = user

    def connection_made(self, transport):
        self.transport = transport
        self.transport.write(json.dumps({"user": self.user, "identifier":
            "LOGIN_REQUEST"}).encode())

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()


async def get_msg(user, client):
    while True:
        line = await aioconsole.ainput(f"{user}:")
        client.transport.write(json.dumps({'identifier': 'MESSAGE', 'message':
            line}).encode())

print("User name:")
user = input()

loop = asyncio.get_event_loop()
client = EchoClientProtocol(user)
coro = loop.create_connection(lambda: client,
                              '127.0.0.1', 8888)
loop.run_until_complete(coro)
loop.run_until_complete(get_msg(user, client))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
client.close()
loop.run_until_complete(client.wait_closed())
loop.close()
