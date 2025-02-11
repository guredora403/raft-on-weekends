import asyncio
from .logger import logger

class State:
    """基本的にはここに必要なメソッドや変数を追加していく"""
    
    def __init__(self, node):
        self.node = node
        self.loop = self.node.loop or asyncio.get_event_loop()
        self.logs = []
        self.statemachine = {}
        self.commited_index = -1
        self.appended_node_counts = {}
        self.commitable_indexes = []

    # サンプルプログラム：ノードから受信したら、カウンターを増やす
    # data: {"sender": "node_name", "data": "data"}
    # sedner: 送信元のノード名
    # data: 送信元から受信したデータ
    def receive(self, data):
        received_from = data["sender"] # 送信元のノード名を取得
        received_message = data["data"] # 送信元から受信したデータを取得
        logger.info("{}からメッセージをもらった！!: {}".format(received_from, received_message))
        from .server import Node
        if self.node.name != "node1":
            if received_message["type"] == "appendlog":
                self.logs.insert(received_message["index"], received_message["data"])
                logger.info(f"add log: {received_message['data']} index: {received_message['index']}")
                for node in Node.cluster:
                    if node.name == "node1":self.loop.create_task(node.send({"type": "appended", "index": received_message["index"]}))
            logger.info(self.logs)
            if received_message["type"] == "commited":
                index = received_message["index"]
                self.statemachine[self.logs[index]["key"]] = self.logs[index]["value"]
                self.commited_index = index
                logger.info("commited current stat: {}".format(self.statemachine))
        else: # リーダ
            if received_message["type"] == "appended":
                index = received_message["index"]
                self.appended_node_counts[index] += 1
                if self.appended_node_counts[index] == 3:
                    self.statemachine[self.logs[index]["key"]] = self.logs[index]["value"]
                    self.commited_index = received_message["index"]
                    logger.info("commited, current state: ".format(self.statemachine))

                    self.loop.create_task(self.node.broadcast({"type": "commited", "index": self.commited_index}))

    # サンプルプログラム：ノード毎にカウンターを5秒ごとに送信する
    # 5秒ごとにノード毎のカウントを自分を除くすべてのノードに送信する
    async def start(self):
        from .server import Node
        if self.node.name == "node1": # 自分がリーダーだったら
            await asyncio.sleep(5)
            log = {
                "key": "x",
                "value": 1,
            }
            await self.new_log(log)
            log = {
                "key": "y",
                "value": 2,
            }
            await self.new_log(log)
            log = {
                "key": "x",
                "value": 3,
            }
            await self.new_log(log)

    async def new_log(self, log):
        self.logs.append(log)
        index = len(self.logs) - 1
        self.appended_node_counts[index] = 1
        logger.info(f"add log: {log} index: {index}")
        logger.info(self.logs)
        await self.node.broadcast({"type": "appendlog", "data": log, "index": index})

    def stop():
        pass