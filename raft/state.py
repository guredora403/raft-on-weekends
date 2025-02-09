import asyncio
from .logger import logger
class State:
    """基本的にはここに必要なメソッドや変数を追加していく"""
    
    def __init__(self, node):
        self.node = node
        self.loop = self.node.loop or asyncio.get_event_loop()
        self.counter = {}

    # data: {"sender": "node_name", "data": "data"}
    # sedner: 送信元のノード名
    # data: 送信元から受信したデータ
    def receive(self, data):
        received_from = data["sender"] # 送信元のノード名を取得
        
        # サンプルプログラム、ノード毎にカウントを増やす
        self.counter[received_from] = max(self.counter.get(received_from, 0), int(data["data"])) + 1

        # ログ出力
        logger.info("Counter[{}] = {}".format(received_from, self.counter[received_from]))

    async def start(self):
        from .server import Node
        while True:
            await asyncio.sleep(5)
            for node in Node.cluster: # Send to all nodes (broadcast)
                if node.is_client: # Don't send to self
                    command = self.counter.get(node.name, 0) # ノード毎のカウントを送信
                    await node.send(command)

    def stop():
        pass