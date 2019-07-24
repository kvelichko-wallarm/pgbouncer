# -*- coding: utf-8 -*-

import pytest
import testinfra
import subprocess
import requests
from prometheus_client.parser import text_string_to_metric_families


@pytest.fixture(scope='module')
def host(docker_compose, request):
    docker_compose_file = request.config.getoption("--docker-compose-file")
    docker_id = subprocess.check_output([
            'docker-compose',
            '-f', docker_compose_file,
            'ps', '-q', 'exporter'
          ]).decode().strip()
    yield testinfra.get_host("docker://"+docker_id)


def test_exporter_process(host):
    pid = host.process.get(pid=1)
    assert pid.args.find(
        "pgbouncer-exporter --config /etc/pgbouncer-exporter/config.yml")


def test_exporter_socket(host):
    assert host.socket("tcp://0.0.0.0:9127").is_listening


def test_request_metrics():
    r = requests.get("http://127.0.0.1:19127/metrics")
    assert r.status_code == 200
    for family in text_string_to_metric_families(r.text):
        if family.name == 'pgbouncer_up':
            assert family.samples[0].value > 0
