import requests
from . import stats_helper

base_url = 'http://127.0.0.1:4001/'
base_url_containers = base_url + 'containers/'


def containers(all_containers=True):
    response = requests.get(
        base_url_containers + 'json',
        {'all': all_containers}
    )
    return response.json()


def container_details(container_id):
    url = base_url_containers + container_id + '/json'
    response = requests.get(url)
    return response.json()


def container_ports(container_id):
    container = container_details(container_id)
    ports = []

    # If container is active, retrieve port bindings from network settings
    if len(container['NetworkSettings']['Ports'].items()) > 0:
        ports_items = container['NetworkSettings']['Ports'].items()
        for port_name, hostPorts in ports_items:
            ports.append({
                'container_port': port_name,
                'host_ip': hostPorts[0]['HostIp'],
                'host_port': hostPorts[0]['HostPort']
            })
    else:
        ports_items = container['HostConfig']['PortBindings'].items()
        for port_name, hostPorts in ports_items:
            ports.append({
                'container_port': port_name,
                'host_ip': '- - - -',
                'host_port': hostPorts[0]['HostPort']
            })

    return ports


def container_stats_raw(container_id):
    url = base_url_containers + container_id + '/stats'
    response = requests.get(url, {'stream': False})
    stats = response.json()

    # Mem usage
    mem_usage = 0
    mem_limit = 0
    if 'usage' in stats['memory_stats'].keys():
        mem_usage = stats_helper.bytes_to_mb(stats['memory_stats']['usage'])
        mem_limit = stats_helper.bytes_to_mb(stats['memory_stats']['limit'])

        # Round to two decimal places
        mem_usage = round(mem_usage, 2)
        mem_limit = round(mem_limit, 0)

    # CPU Usage
    # TODO

    # Network IO
    networks = stats['networks'].items()
    net_stats = []
    for interface_name, transmitted in networks:
        net_stats.append({
            'interface_name': interface_name,
            'rx_data': transmitted['rx_bytes'],
            'tx_data': transmitted['tx_bytes']
        })

    return {
        'container_id': stats['id'],
        'container_name': stats['name'],
        'mem_usage': mem_usage,
        'mem_limit': mem_limit,
        'net_stats': net_stats
    }


def container_stats(container_id):
    url = base_url_containers + container_id + '/stats'
    response = requests.get(url, {'stream': False})
    stats = response.json()

    # Mem usage
    mem_usage = stats['memory_stats']['usage']
    mem_limit = stats['memory_stats']['limit']
    mem_percent = stats_helper.calculate_mem_percent(
        stats['memory_stats']['usage'],
        stats['memory_stats']['limit']
    )

    # CPU Usage percent
    cores = len(stats['cpu_stats']['cpu_usage']['percpu_usage'])
    cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
    system_usage = stats['cpu_stats']['system_cpu_usage']
    prev_cpu = stats['precpu_stats']['cpu_usage']['total_usage']
    prev_system = stats['precpu_stats']['system_cpu_usage']
    cpu_percent = stats_helper.calculate_cpu_percent(
        prev_cpu,
        prev_system,
        cpu_usage,
        system_usage,
        cores
    )

    # Network IO
    networks = stats['networks'].items()
    net_stats = []
    for interface_name, transmitted in networks:
        net_stats.append({
            'interface_name': interface_name,
            'rx_data': stats_helper.bytes_to_human(transmitted['rx_bytes']),
            'tx_data': stats_helper.bytes_to_human(transmitted['tx_bytes'])
        })

    return {
        'mem_usage': stats_helper.bytes_to_human(mem_usage),
        'mem_limit': stats_helper.bytes_to_human(mem_limit),
        'mem_percent': '{}%'.format(mem_percent),
        'pids': stats['pids_stats']['current'],
        'cpu_usage': '{}%'.format(cpu_percent),
        'net_stats': net_stats
    }


def container_start(container_id):
    url = base_url_containers + container_id + '/start'
    response = requests.post(url)
    return response.status_code


def container_stop(container_id):
    url = base_url_containers + container_id + '/stop'
    response = requests.post(url)
    return response.status_code
