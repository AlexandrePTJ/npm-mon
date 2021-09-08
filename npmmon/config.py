from ruyaml import YAML
import os.path


class Config:
    class Cache:
        dir = ''
        log_seek = 'log_seek_pos_cache'
        domain_dt = 'domain_datetime_cache'

        def from_dict(self, d):
            self.dir = d.get('dir', self.dir)
            self.log_seek = d.get('log_seek', self.log_seek)
            self.domain_dt = d.get('domain_dt', self.domain_dt)

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

    logs_dir = ''
    cache = Cache()
    maxmind = MaxMind()
    influxdb = InfluxDB()

    def load_yaml(self, yml_path):
        if os.path.exists(yml_path):
            with open(yml_path, 'r') as fyaml:
                yaml = YAML(typ='safe')
                cfg = yaml.load(fyaml)

                self.logs_dir = cfg.get('logs_dir', '')
                self.cache.from_dict(cfg.get('cache', {}))
                self.maxmind.from_dict(cfg.get('maxmind', {}))
                self.influxdb.from_dict(cfg.get('influxdb', {}))
