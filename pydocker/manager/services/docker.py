import requests

base_url = 'http://127.0.0.1:4001/'
base_url_containers = base_url + 'containers/'


def containers():
    response = requests.get(base_url_containers + 'json', {'all': True})
    return response.json()


def container_details(container_id):
    url = base_url_containers + container_id + '/json'
    response = requests.get(url)
    return response.json()


def start_container(container_id):
    url = base_url_containers + container_id + '/start'
    response = requests.post(url)
    return response.status_code


def stop_container(container_id):
    url = base_url_containers + container_id + '/stop'
    response = requests.post(url)
    return response.status_code
