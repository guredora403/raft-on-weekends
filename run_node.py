import argparse
import raft
import asyncio

async def run(hostname):
    while True:
        await asyncio.sleep(5)
        command = "hello world from {}".format(hostname)
        for node in raft.Node.cluster: # Send to all nodes (broadcast)
            if node.is_client: # Don't send to self
                await node.send(command)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--node')
    parser.add_argument('--cluster')
    args = parser.parse_args()

    hostname = args.node
    node_address = ("0.0.0.0", 8080) # 8080で固定
    cluster_addresses = [(address, 8080) for address in args.cluster.split(',')]


    loop = asyncio.get_event_loop()
    loop.create_task(raft.register_as_server(addresses=[node_address], loop=loop))
    loop.create_task(raft.register_as_client(addresses=cluster_addresses, loop=loop))
    loop.run_until_complete(run(hostname))