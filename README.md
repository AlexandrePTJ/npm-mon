# Nginx Proxy Manager Monitor

Analyze [Nginx Proxy Manager](https://nginxproxymanager.com/) logs and send metrics to InfluxDB.

Currently, it sends:
  - `domain`
  - `scheme`
  - `ip`
  - `city`
  - `country`
  - `latitude`
  - `longitude`

## Usage

As __Nginx Proxy Manager__ is only shipped trough docker, the better option to use this monitor is to use docker too.
However, it can be used directly.

This monitor use a cache system to avoid reading full log files each time it is started, and protect back to the future log entry.

### Configuration

A yaml configuration file and/or environment variables can be use. Configuration is read first, then environment variables may override values.

#### YAML Schema

```yaml
logs:           # NPM logs section
  dir: ''       # Path to NPM logs directory
  domain_rx: '' # Regex to filter domain and sub-domains

cache:    # NPM-Monitor cache section
  dir: '' # Path to cache directory

maxmind:           # MaxMind section
  id: ''           # User ID for querying GeoIP trough Web API
  pk: ''           # User PrivateKey for querying GeoIP trough Web API
  db: ''           # Path to MaxMind city database
  prefer_db: False # Use local database instead of Web API

influxdb:    # InfluxDB section
  host: ''   # Host 
  token: ''  # Token
  org: ''    # Organization
  bucket: '' # Bucket to send metrics
```

#### Environment variables

Environment variables follows YAML schema with this logic: `NPMMON_<section>_<key>`.
So this gives:

- `NPMMON_LOGS_DIR`
- `NPMMON_LOGS_DOMAIN_RX`
- `NPMMON_CACHE_DIR`
- `NPMMON_MAXMIND_ID`
- `NPMMON_MAXMIND_PK`
- `NPMMON_MAXMIND_DB`
- `NPMMON_MAXMIND_PREFER_DB`
- `NPMMON_INFLUXDB_HOST`
- `NPMMON_INFLUXDB_TOKEN`
- `NPMMON_INFLUXDB_ORG`
- `NPMMON_INFLUXDB_BUCKET`

### Docker

Docker image is available by using `alptj/npm-mon`.

In addition to previous environment variables, `NPMMON_CONFIG` is available to set configuration file path.

Two volumes are available:

- `/npmmon/cache`: Where monitoring cache files are stored.
- `/npmmon/logs`: Where NPM logs should be found.

Default configuration sets `NPMMON_CACHE_DIR` to `/npmmon/cache` and `NPMMON_LOGS_DIR` to `/npmmon/logs/logs` (because default npm image use a global volume for `data`).

#### Compose example

_`jc21/nginx-proxy-manager` container is reduced to bare minimal for illustration_

```yaml
version: '3.6'

services:
  app:
    image: jc21/nginx-proxy-manager
    ports:
      - '443:443'
      - '81:81'
    volumes:
      - data:/data

  mon:
    image: alptj/npm-mon
    environment:
      NPMMON_LOGS_DOMAIN_RX: '\w+\.example\.org'
      NPMMON_MAXMIND_DB: /npmmon/GeoLite2-City.mmdb
      NPMMON_MAXMIND_PREFER_DB: 'True'
      NPMMON_INFLUXDB_HOST: influx.mylocal.lan
      NPMMON_INFLUXDB_TOKEN: abcdef
      NPMMON_INFLUXDB_ORG: mylocal
      NPMMON_INFLUXDB_BUCKET: npmmon
    volumes:
      - data:/npmmon/logs:ro
      - moncache:/npmmon/cache
      - ./GeoLite2-City.mmdb:/npmmon/GeoLite2-City.mmdb

volumes:
  data:
  moncache:
```

## TODO

- Add Grafana example
