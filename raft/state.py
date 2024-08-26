import asyncio
from .logger import logger
from .network import convert_ipv4_to_hostname

class State:
    """基本的にはここに必要なメソッドや変数を追加していく"""
    
    def __init__(self, node):
        self.node = node
        self.loop = self.node.loop or asyncio.get_event_loop()
        
        # self.counter = {}

    def request_handler(self, data):
        received_from = convert_ipv4_to_hostname(data["sender"][0])
        
        # # サンプルプログラム、ノード毎にカウントを増やす
        self.counter[received_from] = max(self.counter.get(received_from, 0), int(data["data"])) + 1
        logger.info("Counter[{}] = {}".format(received_from, self.counter[received_from]))

    async def start(self):
        from .server import Node
        while True:
            await asyncio.sleep(5)
            for node in Node.cluster: # Send to all nodes (broadcast)
                if node.is_client: # Don't send to self
                    command = self.counter.get(node.host, 0)
                    await node.send(command)

    def stop():
        pass