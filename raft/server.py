import asyncio
from .network import UDPProtocol

async def register(host, addresses, loop):
    for address in addresses:
        if address not in Node.cluster:
            node = Node(*address, loop)
            client = host != address
            await node.start(client)


def stop():
    for node in Node.cluster:
        node.stop()


class Node:
    """Raft node implementation."""

    cluster = []

    def __init__(self, host, port, loop):
        self.host = host
        self.port = port
        self.loop = loop
        self.request = asyncio.Queue(self.loop)
        self.__class__.cluster.append(self)

    # https://python-doc-ja.github.io/py35/library/asyncio-protocol.html
    async def start(self, client=True):
        protocol = UDPProtocol(queue=self.request, request_handler=self.request_handler, loop=self.loop)
        address = (self.host, self.port)
        print("Starting node on {}:{}".format(address[0], address[1]))
        if client:
            self.transport, _ = await asyncio.Task(
            self.loop.create_datagram_endpoint(protocol, remote_addr=address),
            loop=self.loop
        )
        else:
            self.transport, _ = await asyncio.Task(
            self.loop.create_datagram_endpoint(protocol, local_addr=address),
            loop=self.loop
        )

    def stop(self):
        self.transport.close()

    def request_handler(self, data):
        pass

    async def send(self, data, destination_host, destination_port):
        destination = (destination_host, destination_port)
        await self.request.put({"data": data, "destination": destination})