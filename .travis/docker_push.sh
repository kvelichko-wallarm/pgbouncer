#!/bin/bash

echo "$DOCKER_PASS" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker tag pgbouncer kvelichkowallarm/pgbouncer:$TRAVIS_TAG
docker push kvelichkowallarm/pgbouncer:$TRAVIS_TAG
docker tag pgbouncer kvelichkowallarm/pgbouncer:latest
docker push kvelichkowallarm/pgbouncer:latest
