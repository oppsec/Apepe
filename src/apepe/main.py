from rich import print
from os import path, mkdir, chdir
from pathlib import Path
from zipfile import ZipFile

from androguard.core.bytecodes.apk import APK


def checks(args: str) -> None:
    ''' This function is responsible to check if the APK file exists and if the extension is .apk '''

    file_name: str = args.f
    check_if_file: bool = path.isfile(file_name)
    check_if_file_exists: bool = path.exists(file_name)
    check_extension: bool = file_name.endswith(".apk")

    if not(check_if_file or check_if_file_exists):
        print("[red][!] You have specified an invalid or non existent file or directory[/]")
        return True
    
    if not(check_extension):
        print("[red][!] File extension is not [b].apk[/], please check your input[/]")
        return True

    file_size: int = path.getsize(file_name)

    print(f"[black][-] Checking {file_name}. File size is {file_size}[/]")

    extract_apk(file_name)


def extract_apk(file_name) -> None:
    ''' This function will create a folder called "apk-extracted" and extract the content from the apk file to that folder '''

    normal_dir_name: str = "apk-extracted"
    current_dir = Path.cwd()

    print(f"[black][-] Creating {normal_dir_name} folder to extract the apk...[/]")

    if not(current_dir.joinpath(normal_dir_name).exists()):
        mkdir(normal_dir_name)
        print(f"[green][+] Created {normal_dir_name} folder[/]")

        with ZipFile(file_name, mode="r") as archive:
            archive.extractall(path=normal_dir_name)

        print(f"[green][+] Extracting information from files on apk-extracted folder")
        apk_info_extraction(file_name, normal_dir_name)

    else:
        print(f"[red][!] You already have an [b]{normal_dir_name}[/] folder on this directory, delete or move to another place[/]")
        return True
    

def apk_info_extraction(file_name, normal_dir_name) -> None:
    ''' Use androguard functions (get_package, get_app_name, etc...) to extract normal information from the APK '''

    print(f"\n[black][-] Using androguard to collect APK information[/]")

    apk_file = APK(file_name)

    package_name = apk_file.get_package()
    app_name = apk_file.get_app_name()
    package_signature = apk_file.get_signature_name()
    package_signed = apk_file.is_signed()

    print(f'''[green]
* Package: [white]{package_name}[/white]
* Name: [white]{app_name}[/white]
* Certificate: [white]{package_signature}[/white]
* Signed: [white]{package_signed}[/white]
    [/]''')

    check_app_dev_lang(normal_dir_name)


def check_app_dev_lang(normal_dir_name) -> None:
    ''' Detect the language that the app has been developed through shared object files  '''
    
    chdir(normal_dir_name)
    current_dir = Path.cwd()
    print(f"[black][-] Current directory: {current_dir}[/]")

    ''' Libs Apps '''
    libflutter_file = [f"{current_dir}/lib/x86_64/libflutter.so", 'libflutter.so', 'Flutter']
    libreact_file = [f"{current_dir}/lib/x86_64/libreact_config.so", 'libreact_config.so', 'React Native']
    second_libreact_file = [f"{current_dir}/lib/x86_64/libreact_utils.so", 'libreact_utils.so', 'React Native']

    libraries = [libflutter_file, libreact_file, second_libreact_file]

    for library in libraries:
        lib_path = library[0]
        lib_file_name = library[1]
        app_lang = library[2]

        if(path.exists(lib_path) == True):
            print(f"[green][+] [b]{lib_file_name}[/b] found. App is probably built with [b]{app_lang}[/b][/]")
        else:
            print(f"[black][-] [b]{lib_file_name}[/b] not found. Skipping...[/]")

    print("\n[yellow][!] Done, exiting... [/]")