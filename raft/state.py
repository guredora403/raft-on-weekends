import asyncio
from .logger import logger
class State:
    """基本的にはここに必要なメソッドや変数を追加していく"""
    
    def __init__(self, node):
        self.node = node
        self.loop = self.node.loop or asyncio.get_event_loop()
        self.counter = {}


    # サンプルプログラム：ノードから受信したら、カウンターを増やす
    # data: {"sender": "node_name", "data": "data"}
    # sedner: 送信元のノード名
    # data: 送信元から受信したデータ
    def receive(self, data):
        received_from = data["sender"] # 送信元のノード名を取得
        received_data = data["data"] # 送信元から受信したデータを取得
        
        # サンプルプログラム、ノード毎にカウントを増やす
        self.counter[received_from] = max(self.counter.get(received_from, 0), int(received_data)) + 1

        # ログ出力
        logger.info("Counter[{}] = {}".format(received_from, self.counter[received_from]))

    # サンプルプログラム：ノード毎にカウンターを5秒ごとに送信する
    # 5秒ごとにノード毎のカウントを自分を除くすべてのノードに送信する
    async def start(self):
        from .server import Node
        while True:
            await asyncio.sleep(5)
            for node in Node.cluster: 
                if node.is_client: # 自分を除くすべてのノードに送信
                    command = self.counter.get(node.name, 0) # ノード毎のカウントを取得
                    await node.send(command) # データ送信

    def stop():
        pass