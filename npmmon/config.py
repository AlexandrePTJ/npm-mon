# coding: utf-8

import os
import os.path
from ruyaml import YAML


class Config:

    @staticmethod
    def _get_env_key(section, key):
        return f'NPMMON_{section}_{key}'.upper()

    class Logs:
        dir = ''
        domain_rx = ''

        def from_dict(self, d):
            self.dir = d.get('dir', self.dir)
            self.domain_rx = d.get('domain_rx', self.domain_rx)

        def from_env(self):
            self.dir = os.environ.get(Config._get_env_key('logs', 'dir'), self.dir)
            self.domain_rx = os.environ.get(Config._get_env_key('logs', 'domain_rx'), self.domain_rx)

    class Cache:
        dir = ''
        log_seek = 'log_seek_pos_cache'
        domain_dt = 'domain_datetime_cache'

        def from_dict(self, d):
            self.dir = d.get('dir', self.dir)
            self.log_seek = d.get('log_seek', self.log_seek)
            self.domain_dt = d.get('domain_dt', self.domain_dt)

        def from_env(self):
            self.dir = os.environ.get(Config._get_env_key('cache', 'dir'), self.dir)
            self.log_seek = os.environ.get(Config._get_env_key('cache', 'log_seek'), self.log_seek)
            self.domain_dt = os.environ.get(Config._get_env_key('cache', 'domain_dt'), self.domain_dt)

    class MaxMind:
        id = 0
        pk = ''
        db = ''
        prefer_db = False

        def from_dict(self, d):
            self.id = d.get('id', self.id)
            self.pk = d.get('pk', self.pk)
            self.db = d.get('db', self.db)
            self.prefer_db = d.get('prefer_db', self.prefer_db)

        def from_env(self):
            self.id = os.environ.get(Config._get_env_key('maxmind', 'id'), self.id)
            self.pk = os.environ.get(Config._get_env_key('maxmind', 'pk'), self.pk)
            self.db = os.environ.get(Config._get_env_key('maxmind', 'db'), self.db)
            self.prefer_db = os.environ.get(Config._get_env_key('maxmind', 'prefer_db'), self.prefer_db)

    class InfluxDB:
        host = ''
        token = ''
        org = ''
        bucket = ''

        def from_dict(self, d):
            self.host = d.get('host', self.host)
            self.token = d.get('token', self.token)
            self.org = d.get('org', self.org)
            self.bucket = d.get('bucket', self.bucket)

        def from_env(self):
            self.host = os.environ.get(Config._get_env_key('influxdb', 'host'), self.host)
            self.token = os.environ.get(Config._get_env_key('influxdb', 'token'), self.token)
            self.org = os.environ.get(Config._get_env_key('influxdb', 'org'), self.org)
            self.bucket = os.environ.get(Config._get_env_key('influxdb', 'bucket'), self.bucket)

    logs = Logs()
    cache = Cache()
    maxmind = MaxMind()
    influxdb = InfluxDB()

    def load_yaml(self, yml_path):
        if os.path.exists(yml_path):
            with open(yml_path, 'r') as fyaml:
                yaml = YAML(typ='safe')
                cfg = yaml.load(fyaml)

                self.logs.from_dict(cfg.get('logs', {}))
                self.cache.from_dict(cfg.get('cache', {}))
                self.maxmind.from_dict(cfg.get('maxmind', {}))
                self.influxdb.from_dict(cfg.get('influxdb', {}))

    def load_from_env(self):
        self.logs.from_env()
        self.cache.from_env()
        self.maxmind.from_env()
        self.influxdb.from_env()
