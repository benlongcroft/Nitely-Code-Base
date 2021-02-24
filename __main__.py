from nitely_core.cli import cli
from nitely_core import start_NITE

def main(kwargs):
    nite = start_NITE(kwargs)

if __name__ == '__main__':
    packages = main(*cli())
