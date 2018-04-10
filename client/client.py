import asyncio
import aioconsole
import json


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, user, loop):
        self.user = user
        self.transport = None
        self.loop = loop

    def connection_made(self, transport):
        self.transport = transport
        self.transport.write(json.dumps({"player": self.user, "identifier": "LOGIN_REQUEST"}).encode())

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()


async def get_msg(user, client):
    while True:
        line = await aioconsole.ainput(f"{user}:")
        if line == 'keys':
            client.transport.write(json.dumps({'identifier': 'KEYS_PRESSED', 'keys_pressed':{'up':True}, 'player':'hr0m'}).encode())
        else:
            client.transport.write(line.encode())

print("User name:")
user_name = input()

main_loop = asyncio.get_event_loop()
client_protocol = EchoClientProtocol(user_name, main_loop)
coro = main_loop.create_connection(lambda: client_protocol, '127.0.0.1', 8889)
main_loop.run_until_complete(coro)
process = main_loop.run_until_complete(get_msg(user_name, client_protocol))
try:
    main_loop.run_forever()
except KeyboardInterrupt:
    pass
process.close()
main_loop.run_until_complete(process.wait_closed())
main_loop.close()
