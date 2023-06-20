from src.apepe.interface.ui import get_banner
from src.apepe.main import checks

from argparse import ArgumentParser

if __name__ == "__main__":

    get_banner()

    parser = ArgumentParser()
    parser.add_argument('-f', help='Specify the APK file path/name', required=True)
    args = parser.parse_args()

    checks(args)

