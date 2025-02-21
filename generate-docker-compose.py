import sys
import yaml
import json

def generate_docker_compose(num_nodes):
    services = {}
    network_name = 'raft-network'
    host_base_port = 3333

    node_portlist = {}

    for i in range(1, num_nodes + 1):
        node_name = f'node{i}'
        cluster = ','.join([f'node{j}' for j in range(1, num_nodes + 1) if j != i])
        ipv4_address = f'10.0.0.{i+1}'
        host_port = host_base_port + i - 1
        services[node_name] = {
            'build': '.',
            'container_name': node_name,
            'environment': [
                f'NODE={node_name}',
                f'CLUSTER={cluster}'
            ],
            'ports': [f'{host_port}:8080/udp'],
            'command': ["python", "run_node.py", "--node", ipv4_address, "--cluster", cluster, "--name", node_name],
            'networks': {
                network_name: {
                    'ipv4_address': ipv4_address
                }
            }
        }
        node_portlist[node_name] = host_port

    docker_compose = {
        'version': '3.8',
        'services': services,
        'networks': {
            network_name: {
                'driver': 'bridge',
                'ipam': {
                    'driver': 'default',
                    'config': [
                        {'subnet': '10.0.0.0/24'}
                    ]
                }
            }
        }
    }


    # Write the docker-compose.yml file
    with open('docker-compose.yml', 'w') as file:
        yaml.dump(docker_compose, file, default_flow_style=False)
    with open('node_portlist.json', 'w') as file:
        json.dump(node_portlist, file)
    print(f'docker-compose.yml with {num_nodes} nodes generated successfully.')
    print(f'node_portlist.json with {num_nodes} nodes generated successfully.')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python generate_docker_compose.py <number_of_nodes (< 254)>")
        sys.exit(1)

    try:
        num_nodes = int(sys.argv[1])
        if num_nodes < 1 or num_nodes > 253:
            raise ValueError
        generate_docker_compose(num_nodes)
    except ValueError:
        print("Please provide a valid integer for the number of nodes (< 254).")
        sys.exit(1)
