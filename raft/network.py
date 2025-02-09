import asyncio
from .serializers import MessagePackSerializer
from .logger import logger

class UDPProtocol(asyncio.DatagramProtocol):
    def __init__(self, queue, request_handler, loop):
        self.queue = queue
        self.request_handler = request_handler
        self.serializer = MessagePackSerializer
        self.loop = loop or asyncio.get_event_loop()

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
       logger.info('Received %r from %s' % (data, addr[0]))
       data.update({"sender": self._convert_ipv4_to_name(addr[0])})
       self.request_handler(data)

    def error_received(self, exc):
        logger.error('Error received:', exc)

    def connection_lost(self, exc):
        logger.warning('Connection lost:', exc)
        
    def _convert_ipv4_to_name(self, ip):
        node_id = str(int(ip.split('.')[3])-1)
        return f"node{node_id}"