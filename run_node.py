import argparse
import raft
import asyncio

async def run(node_address):
    while True:
        await asyncio.sleep(5)
        command = "hello world from {}".format(node_address[0])
        for node in raft.Node.cluster: # Send to all nodes (broadcast)
            address = (node.host, node.port)
            if address != node_address: # Don't send to self
                print(address)
                await node.send(command, *address)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--node')
    parser.add_argument('--cluster')
    args = parser.parse_args()

    node_address = (args.node, 8080) # 8080で固定
    cluster_addresses = [(address, 8080) for address in args.cluster.split(',') if address != args.node]


    loop = asyncio.get_event_loop()
    loop.create_task(raft.register(host=node_address, addresses=cluster_addresses, loop=loop))
    loop.run_until_complete(run(node_address))