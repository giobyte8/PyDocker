# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from manager.services import docker


@csrf_exempt
def container_start(req):
    container_id = req.POST.get('container_id')
    code = docker.container_start(container_id)

    return HttpResponse(status=code)


@csrf_exempt
def container_stop(req):
    container_id = req.POST.get('container_id')
    code = docker.container_stop(container_id)

    return HttpResponse(status=code)


def stats(req):
    all_stats = []

    containers = docker.containers(False)
    for container in containers:
        c_stats = docker.container_stats_raw(container['Id'])
        all_stats.append(c_stats)
    return JsonResponse(all_stats, safe=False)
