from datetime import datetime
import geoip2.database
from geoip2.errors import GeoIP2Error
import geoip2.webservice
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os.path
import re
import shelve


NPM_LOG_LINE_REGEX = (r'\[(?P<datetime>.*?)\].*(?P<scheme>http[s]?)\s(?P<domain>\w+\.bouledemilk\.ovh)'
                      '.*\[Client (?P<ip>.*?)\].*')
NPM_LOG_DATETIME_FMT = '%d/%b/%Y:%H:%M:%S %z'


class Processor:

    def __init__(self, cfg):
        # Cache files for log file position (like tail -f) and avoid redundant insert
        self._log_seek_pos_cache = shelve.open(os.path.join(cfg.cache.dir, cfg.cache.log_seek))
        self._domain_datetime_cache = shelve.open(os.path.join(cfg.cache.dir, cfg.cache.domain_dt))

        # Compile most used regex
        self._rx_access_infos = re.compile(NPM_LOG_LINE_REGEX)

        # GeoIP2 client
        if cfg.maxmind.prefer_db and os.path.exists(cfg.maxmind.db):
            self._maxmind_client = geoip2.database.Reader(cfg.maxmind.db)
        else:
            self._maxmind_client = geoip2.webservice.Client(cfg.maxmind.id, cfg.maxmind.pk, host='geolite.info')

    def __del__(self):
        if self._log_seek_pos_cache:
            self._log_seek_pos_cache.close()
        if self._domain_datetime_cache:
            self._domain_datetime_cache.close()

    def analyze_log_file(self, log_path, from_tail=True):
        prev_seek_pos = self._log_seek_pos_cache.get(log_path, None)
        current_size = os.path.getsize(log_path)

        # Nothing to read, may break cache info.
        if current_size == 0:
            return

        # Log rotation
        if prev_seek_pos is None:
            prev_seek_pos = current_size if from_tail else 0
        if prev_seek_pos > current_size:
            prev_seek_pos = 0

        # Read and process new lines
        with open(log_path, 'r') as f_log_path:
            f_log_path.seek(prev_seek_pos, 0)

            for line in f_log_path:
                self._process_line(line)
            prev_seek_pos = f_log_path.tell()

        # Update pos in file
        self._log_seek_pos_cache[log_path] = prev_seek_pos

    def _process_line(self, line):
        r = self._rx_access_infos.match(line)
        if r:
            dt = datetime.strptime(r.group('datetime'), NPM_LOG_DATETIME_FMT)
            last_dt_access = self._domain_datetime_cache.get(r.group('domain'), None)
            if last_dt_access is None or dt > last_dt_access:
                self._domain_datetime_cache[r.group('domain')] = dt
                self._record_log_entry(*r.groups())

    def _get_location_from_ip(self, ip):
        try:
            response = self._maxmind_client.city(ip)
            return response.country.name, response.city.name, response.location.latitude, response.location.longitude
        except GeoIP2Error as e:
            print(e)
        finally:
            return '', '', '', ''

    def _record_log_entry(self, logts, scheme, domain, ip):
        country, city, latitude, longitude = self._get_location_from_ip(ip)
        print(f'datetime: {logts}\nscheme: {scheme}\ndomain: {domain}\nip: {ip}\ncountry: {country}\ncity: {city}')
