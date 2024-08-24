import asyncio
from .network import UDPProtocol


async def register_as_server(addresses, loop):
    for address in addresses:
        if address not in Node.cluster:
            node = Node(*address, loop, is_client=False)
            await node.start()

async def register_as_client(addresses, loop):
    for address in addresses:
        if address not in Node.cluster:
            node = Node(*address, loop, is_client=True)
            await node.start()


def stop():
    for node in Node.cluster:
        node.stop()


class Node:
    """Raft node implementation."""

    cluster = []

    def __init__(self, host, port, loop, is_client=False):
        self.host = host
        self.port = port
        self.loop = loop
        self.is_client = is_client
        self.request = asyncio.Queue()
        self.__class__.cluster.append(self)

    # https://python-doc-ja.github.io/py35/library/asyncio-protocol.html
    async def start(self):
        protocol = UDPProtocol(queue=self.request, request_handler=self.request_handler, loop=self.loop)
        address = (self.host, self.port)
        if self.is_client:
            self.transport, _ = await asyncio.Task(
            self.loop.create_datagram_endpoint(protocol, remote_addr=address),
            loop=self.loop)
            print("Connecting to {}:{}".format(address[0], address[1]))
        else:
            self.transport, _ = await asyncio.Task(
            self.loop.create_datagram_endpoint(protocol, local_addr=address),
            loop=self.loop)
            print("Starting node on {}:{}".format(address[0], address[1]))

    def stop(self):
        self.transport.close()

    def request_handler(self, data):
        print("Received data: {}".format(data))
        pass

    async def send(self, data):
        if not self.is_client:
            raise Exception("Only clients can send data")
        await self.request.put({"data": data})