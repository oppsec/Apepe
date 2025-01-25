from argparse import ArgumentParser
from pathlib import Path
from src.apepe.interface.ui import get_banner
from src.apepe.main import perform_checks

def main() -> None:
    """ 
    This functions aims to print the banner for the user and handle
    all the possible arguments for the tool. 
    """

    get_banner()

    parser = ArgumentParser()
    parser.add_argument('-f', help='Specify the APK file path/name', required=True)
    parser.add_argument('-l', help='List suggested SSL pinnings scripts', required=False, action='store_true')
    parser.add_argument('-d', help='Enumerate deeplinks', required=False, action='store_true')
    args = parser.parse_args()

    apk_file = args.f
    list_scripts = args.l
    apk_file = str(Path(apk_file).resolve())
    deeplink = args.d

    perform_checks(apk_file, list_scripts, deeplink)

if __name__ == "__main__":
    main()