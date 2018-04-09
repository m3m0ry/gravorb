import asyncio
import json

class GameServer():
    def __init__(self):
        self.connections = []

    def broadcast(self, message):
        for connection in self.connections:
            connection.write(message.encode())

class ServerProtocol(asyncio.Protocol):
    def __init__(self, server):
        self.server = server

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
        self.server.connections.append(transport)

    def handle_login(self, message):
        self.transport.write(json.dumps({'identifier': 'LOGIN_RESPONSE',
            'message': 'Hello {!s}'.format(message['user'])}).encode())

    def message(self, message):
        self.server.broadcast(message['message'])

    def logout(self):
        self.transport.close()

    def data_received(self, data):
        if not data:
            self.transport.write(json.dumps({'error': 'NO_DATA'}).encode())
        message = json.loads(data.decode())
        print(message)
        identifier = message['identifier']
        if identifier == "LOGIN_REQUEST":
            self.handle_login(message)
        elif identifier == 'MESSAGE':
            self.message(message)
        elif identifier == 'KEY_PRESSED':
            self.transport.write(json.dumps({"test": payload}).encode())
        elif identifier == 'QUIT':
            self.logout(payload)
        else:
            self.transport.write('no such identifier\n'.encode())

    def handle

    def eof_received(self):
        print('Got eof')

    def connection_lost(self, exc):
        print('Lost:', exc)

loop = asyncio.get_event_loop()
game_server = GameServer()
# Each client connection will create a new protocol instance
coro = loop.create_server(lambda: ServerProtocol(game_server), '127.0.0.1', 8888)
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
