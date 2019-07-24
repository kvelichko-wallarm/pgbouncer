[![Build Status](https://travis-ci.com/kvelichko-wallarm/pgbouncer.svg?branch=master)](https://travis-ci.com/kvelichko-wallarm/pgbouncer)

Pgbouncer
=========

PgBouncer is a lightweight connection pooler for PostgreSQL.

Install the Chart
-----------------

To install the chart with the releases name `my-release` in namespace `my-namespace`:
```bash
 $ helm install -n my-release --namespace my-namespace wallarm/pgbouncer
```

Configuration example
---------------------

### Yandex cloud configuration

```yaml
imagePullSecrets:
  - name: <Secretname>
config:
  adminPassword: <SomePassword>
  databases:
    <DBName1>:
      host: <HostName1>.mdb.yandexcloud.net
      port: 6432
    <DBName2>:
      host: <HostName2>.mdb.yandexcloud.net
      port: 6432
    <DBName3>:
      host: <HostName3>.mdb.yandexcloud.net
      port: 6432
  pgbouncer:
    server_tls_sslmode: prefer
  userlist:
    <DBUser1>: <md5MD5HashOfPassword1>
    <DBUser2>: <md5MD5HashOfPassword2>
    <DBUSer3>: <md5MD5HashOfPassword3>
```

Configuration
-------------

The following table lists the configurable parameters of the Prometheus chart and their default values.

Parameter | Description | Default
--------- | ----------- | -------
`replicaCount` | desired number of pgbouncer pods | `1`
`imagePullSecrets` | container image pull secrets | `[]`
`image.repository` | pgbouncer container image repository | `wallarm-dkr-infra.jfrog.io/pgbouncer`
`image.tag` | pgbouncer container image tag | `0.3.0`
`image.pullPolicy` | pgbouncer container image pull policy | `Always`
`nameOverride` | override .Chart.Name with this name | `""`
`fullnameOverride` | override fullname with this name | `""`
`service.type` | type of pgbouncer service to create | `ClusterIP`
`service.port` | pgbouncer headless service port | `5432`
`resources` | pgbouncer pod resource requests & limits | `{}`
`nodeSelector` | node labels for pgbouncer pod assignment | `{}`
`tolerations` | node taints to tolerate (requires Kubernetes >=1.6) | `[]`
`affinity` | pod affinity | `{}`
`config.adminUser` | Set pgbouncer `admin_user` option. `admin_user` - database user that are allowed to connect and run all commands on console. | `admin`
`config.adminPassword` | Set password for `admin_user` | `""`
`config.authUser` | Set pgbouncer `auth_user` option. If `auth_user` is set, any user not specified in `auth_file` will be queried through the `auth_query` query from `pg_shadow` in the database using `auth_user` | `""`
`config.authPassword` | Set password for `auth_user` | `""`
`config.databases` | Dict of database connections string described in section `[databases]` in pgbouncer.ini file | `{}`
`config.pgbouncer` | Dict of pgbouncer options described in section `[pgbouncer]` in pgbouncer.ini file | 
`config.pgbouncer.auth_type` | Set option `auth_type` | `md5`
`config.pgbouncer.pool_mode` | Set option `pool_mode` | `transaction`
`config.pgbouncer.max_client_conn` | Set option `max_client_conn` | `1024`
`config.pgbouncer.default_pool_size` | Set option `default_pool_size` | `20`
`config.userlist` | Dict of users for `userlist.txt` file | `{}`
`pgbouncerExporter.name` | pgbouncer exporter container name suffix | `exporter`
`pgbouncerExporter.port` | pgbouncer exporter port | `9127`
`pgbouncerExporter.image.repository` | pgbouncer exporter image repository | `spreaker/prometheus-pgbouncer-exporter`
`pgbouncerExporter.image.tag` | pgbouncer exporter image tag | `2.0.1`
`pgbouncerExporter.image.pullPolicy` | pgbouncer exporter image pull policy | `IfNotPresent`

Development Tips
----------------

Install PostgreSQL in kubernetes:
```
$ kubectl create namespace pgbouncer
$ kubectl -n pgbouncer apply -f tools/kubernetes-pg.yaml
$ helm install -n prometheus --namespace pgbouncer stable/prometheus
```

Перед следующим шагом создайте секрет с именем wallarm-dkr-infra-key для доступа к хранилищц докер-образов:
```
$ helm install -n pgbouncer --namespace pgbouncer helm/pgbouncer -f tools/values.yaml
```

Test helm with kubeval:
```
$ helm template helm/pgbouncer/ -f tools/values.yaml --output-dir manifest/
$ find manifest/ -name '*.yaml' | xargs kubeval
```
