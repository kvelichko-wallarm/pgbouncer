# -*- coding: utf-8 -*-

import pytest
import testinfra
import subprocess
import psycopg2


@pytest.fixture(scope='module')
def host(docker_compose, request):
    docker_compose_file = request.config.getoption("--docker-compose-file")
    docker_id = subprocess.check_output([
            'docker-compose',
            '-f', docker_compose_file,
            'ps', '-q', 'pgbouncer'
          ]).decode().strip()
    yield testinfra.get_host("docker://"+docker_id)


def test_pgbouncer_process(host):
    pid = host.process.get(pid=1)
    assert pid.args == "pgbouncer /etc/pgbouncer/pgbouncer.ini"


def test_pgbouncer_socket(host):
    assert host.socket("tcp://0.0.0.0:5432").is_listening


def test_pgbouncer_admin():
    connection = psycopg2.connect(
                    user='admin',
                    password='xaod4yeeS5ohsh7chaesh0Quichauv8o',
                    host='127.0.0.1',
                    port=16432,
                    database='pgbouncer'
                )
    connection.set_isolation_level(0)
    cursor = connection.cursor()
    cursor.execute("SHOW CONFIG;")
    connection.commit()
    record = cursor.fetchall()
    cursor.close()
    connection.close()
    assert len(record) > 0


def test_pgbouncer_database():
    connection = psycopg2.connect(
                    user='test',
                    password='qwerty',
                    host='127.0.0.1',
                    port=16432,
                    database='testdb'
                )
    connection.set_isolation_level(0)
    cursor = connection.cursor()
    cursor.execute("SELECT 1;")
    connection.commit()
    record = cursor.fetchall()
    cursor.close()
    connection.close()
    print(record[0])
    assert record[0] == (1,)
