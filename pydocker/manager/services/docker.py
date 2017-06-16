import requests

url_api_docker = 'http://127.0.0.1:4001/'


def containers():
    response = requests.get(url_api_docker + 'containers/json', {'all': True})
    return response.json()


def start_container(container_id):
    url = url_api_docker + 'containers/' + container_id + '/start'
    response = requests.post(url)
    return response.status_code


def stop_container(container_id):
    url = url_api_docker + 'containers/' + container_id + '/stop'
    response = requests.post(url)
    return response.status_code
