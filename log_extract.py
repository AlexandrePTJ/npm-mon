from npmmon.config import Config
from npmmon.runner import ReadAllRunner


if __name__ == "__main__":

    cfg = Config()
    cfg.load_yaml('config.yml')

    readAllRunner = ReadAllRunner(cfg)
    readAllRunner.run()
