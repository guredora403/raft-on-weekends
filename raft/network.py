import asyncio
from .serializers import MessagePackSerializer

class UDPProtocol(asyncio.DatagramProtocol):
    def __init__(self, queue, request_handler, loop):
        self.queue = queue
        self.request_handler = request_handler
        self.serializer = MessagePackSerializer
        self.loop = loop

    def __call__(self):
        return self

    async def start(self):
        while not self.transport.is_closing():
            request = await self.queue.get()
            data = self.serializer.pack(request)
            self.transport.sendto(data, None)

    def connection_made(self, transport):
        self.transport = transport
        asyncio.ensure_future(self.start(), loop=self.loop)

    def datagram_received(self, data, addr):
       data = self.serializer.unpack(data)
       data.update({"sender": addr})
       self.request_handler(data)

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print('Connection lost:', exc)