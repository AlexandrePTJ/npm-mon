import time
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler

from .processor import Processor

NPM_LOGS_FILENAME_REGEX = r'.*proxy-host-\d+_access.log'


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
        self._observer.schedule(self._handler, self._cfg.logs_dir, recursive=False)
        self._observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self._observer.stop()
            print("Observer Stopped")
        finally:
            self._observer.join()
