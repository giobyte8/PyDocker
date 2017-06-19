# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from services import docker


def index(req):
    containers = docker.containers()

    # Assembly context
    params = {
        'containers': containers,
        'nav_active': 'containers'
    }

    return render(req, 'manager/containers/index.html', params)


def containers_grid(req):
    if req.is_ajax():
        containers = docker.containers()

        # Assembly context
        params = {
            'containers': containers,
        }

        html = render_to_string('manager/components/containers_grid.html', params)
        return HttpResponse(html)
    else:
        return redirect('index')


def container_details(req):
    container_id = req.GET.get('container_id')
    params = {
        'container': docker.container_details(container_id),
        'container_ports': docker.container_ports(container_id),
        'container_stats': docker.container_stats(container_id)
    }
    return render(req, 'manager/containers/detail.html', params)
