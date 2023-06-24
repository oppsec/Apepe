from argparse import ArgumentParser

from src.apepe.interface.ui import get_banner
from src.apepe.main import perform_checks

def main() -> None:
    """ Main function from the script """

    get_banner()

    parser = ArgumentParser()
    parser.add_argument('-f', help='Specify the APK file path/name', required=True)
    parser.add_argument('-l', help='List suggested SSL pinnings scripts', required=False, action='store_true')
    args = parser.parse_args()

    apk_file = args.f
    list_scripts = args.l

    perform_checks(apk_file, list_scripts)

if __name__ == "__main__":
    main()