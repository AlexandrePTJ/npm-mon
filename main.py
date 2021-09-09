import argparse
from npmmon.config import Config
from npmmon.runner import LogsTailRunner, ReadAllRunner

# Parse args
parser = argparse.ArgumentParser(description='NPM IP monitor')
parser.add_argument('-c', '--config', action='store', required=True)
parser.add_argument('-w', '--watch', action='store_true')
args = parser.parse_args()

# Load config
config = Config()
config.load_yaml(args.config)

# Run
runner = LogsTailRunner(config) if args.watch else ReadAllRunner(config)
runner.run()
