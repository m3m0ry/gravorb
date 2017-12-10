import asyncio


async def tcp_echo_client(message, loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888,
                                                   loop=loop)
    while True:


        print('Send: %r' % message)
        writer.write(message.encode())
        await writer.drain()
        #writer.close()

        data = await reader.read(100)
        print('Received: %r' % data.decode())


message = 'new_player hr0m\n'
loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(message, loop))
loop.close()
