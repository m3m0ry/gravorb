import asyncio
import sys
import re


class GameServer:
    def __init__(self, server_name, port, loop):
        self.server_name = server_name
        self.connections = {}
        self.server = loop.run_until_complete(
                asyncio.start_server(
                    self.accept_connection, "", port, loop=loop))

    async def accept_connection(self, reader, writer):
        username = (await self.prompt_username(reader, writer))
        if username is not None:
            print("User %r has joined the room" % (username,))
            await self.handle_connection(username, reader)
            print("User %r has left the room" % (username,))
        await writer.drain()
        writer.close()

    def broadcast(self, message):
        for reader, writer in self.connections.values():
            writer.write((message + "\n").encode("utf-8"))

    async def prompt_username(self, reader, writer):
        try:
            data = (await reader.readline()).decode("utf-8").strip()
            if not data:
                return None
            username = re.match('new_player\s*(\w*)', data)[1]
            print(username)
            if username not in self.connections:
                self.connections[username] = (reader, writer)
                return username
            else:
                writer.write('error "Username already in use"\n'.encode('utf-8'))
                return None
        except (UnicodeDecodeError, TypeError) as e:
            writer.write('error "No user name provided"\n'.encode("utf-8"))

    async def handle_connection(self, username, reader):
        while True:
            try:
                data = (await reader.readline()).decode("utf-8")
            except UnicodeDecodeError:
                continue
            if not data:
                del self.connections[username]
                return None
            self.broadcast(username + ": " + data.strip())


def main(argv):
    loop = asyncio.get_event_loop()
    server = GameServer("Test Server", 8888, loop)
    try:
        loop.run_forever()
    finally:
        loop.close()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
