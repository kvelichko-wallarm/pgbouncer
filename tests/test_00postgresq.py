# -*- coding: utf-8 -*-

import pytest
import testinfra
import subprocess
import time


@pytest.fixture(scope='module')
def host(docker_compose, request):
    docker_compose_file = request.config.getoption("--docker-compose-file")
    docker_id = subprocess.check_output([
            'docker-compose',
            '-f', docker_compose_file,
            'ps', '-q', 'pg'
          ]).decode().strip()
    yield testinfra.get_host("docker://"+docker_id)


def test_wait_for_postgres(host):
    cmd = ("until psql -U postgres -c '\\q'; do \n"
           ">&2 echo \"Postgres is unavailable - sleeping\"\n"
           "sleep 1\n"
           "done\n")
    host.check_output(cmd, shell=True)
    time.sleep(2)


def test_postgres_process(host):
    pg = host.process.filter(comm='postgres')
    assert len(pg) > 1


def test_postgres_socket(host):
    assert host.socket("tcp://0.0.0.0:5432").is_listening
