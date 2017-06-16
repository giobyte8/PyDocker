# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from manager.services import docker


@csrf_exempt
def start_container(req):
    container_id = req.POST.get('container_id')
    code = docker.start_container(container_id)

    return HttpResponse(status=code)


@csrf_exempt
def stop_container(req):
    container_id = req.POST.get('container_id')
    code = docker.stop_container(container_id)

    return HttpResponse(status=code)
