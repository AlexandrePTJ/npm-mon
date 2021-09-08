from npmmon.config import Config
from npmmon.runner import LogsTailRunner


if __name__ == "__main__":

    cfg = Config()
    cfg.load_yaml('config.yml')

    logsTailRunner = LogsTailRunner(cfg)
    logsTailRunner.run()
