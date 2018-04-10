import asyncio
import json
import numpy as np
import random

from player import Player


class GameServer:
    def __init__(self):
        self.connections = {}
        self.players = {}
        self.map = np.random.randint(2, size=(20, 20))

    def logout(self, connection):
        player = self.connections.pop(connection)
        del self.players[player]
        return player


class ServerProtocol(asyncio.Protocol):
    def __init__(self, game_server):
        self.server = game_server
        self.transport = None

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def handle_login(self, message):
        self.server.connections[self.transport] = message['player']
        self.server.players[message['player']] = Player(np.random.rand(2), random.random())
        self.transport.write(json.dumps({'identifier': 'LOGIN_RESPONSE',
                                         'map': self.server.map.tolist()}).encode())
        print('New player {!s}'.format(message['player']))

    def keys_pressed(self, message):
        for k, v in message['keys_pressed'].items():
            self.server.players[message['player']].keys_pressed[k] = v
        self.transport.write(json.dumps({'players': {name: player.position.tolist() for name, player in self.server.players.items()}}).encode())

    def data_received(self, data):
        if not data:
            self.transport.write(json.dumps({'error': 'NO_DATA'}).encode())
        message = data.decode()
        print(message)
        message = json.loads(message)
        identifier = message['identifier']
        if identifier == "LOGIN_REQUEST":
            self.handle_login(message)
        elif identifier == 'KEYS_PRESSED':
            self.keys_pressed(message)
        else:
            self.transport.write(json.dumps({'error': 'NO_SUCH_IDENTIFIER'}).encode())

    def connection_lost(self, exc):
        player = self.server.logout(self.transport)
        self.transport.close()
        print('Lost:', player, exc)


loop = asyncio.get_event_loop()
gs = GameServer()
# Each client connection will create a new protocol instance
coro = loop.create_server(lambda: ServerProtocol(gs), '127.0.0.1', 8889)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
