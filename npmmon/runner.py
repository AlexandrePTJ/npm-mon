# coding: utf-8

import asyncio
import os
import os.path
import re

from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler

from .processor import Processor

NPM_LOGS_FILENAME_REGEX = r'.*proxy-host-\d+_access.log$'


class LogsTailRunner:

    class NPMLogsEventHandler(RegexMatchingEventHandler):

        def __init__(self, cfg):
            super().__init__(regexes=[NPM_LOGS_FILENAME_REGEX], ignore_directories=True)
            self._logs_processor = Processor(cfg)

        def on_modified(self, event):
            self._logs_processor.analyze_log_file(event.src_path)

    def __init__(self, cfg):
        self._handler = LogsTailRunner.NPMLogsEventHandler(cfg)
        self._observer = Observer()
        self._cfg = cfg

    def run(self):
        self._observer.schedule(self._handler, self._cfg.logs.dir, recursive=False)
        self._observer.start()
        loop = asyncio.get_event_loop()
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self._observer.stop()
            self._observer.join()


class ReadAllRunner:
    def __init__(self, cfg):
        self._cfg = cfg

    def run(self):
        processor = Processor(self._cfg)
        rx_fname = re.compile(NPM_LOGS_FILENAME_REGEX)
        with os.scandir(self._cfg.logs.dir) as it:
            for entry in it:
                if rx_fname.match(entry.name) and entry.is_file():
                    print('Process %s' % entry.name)
                    processor.analyze_log_file(os.path.join(self._cfg.logs.dir, entry.name), from_tail=False)
