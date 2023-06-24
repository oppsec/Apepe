from rich import print
from os import path, mkdir, chdir
from pathlib import Path
from zipfile import ZipFile

from androguard.core.bytecodes.apk import APK
from androguard.core.bytecodes.dvm import DalvikVMFormat

from src.apepe.modules.suggest import suggest_sslpinning

def perform_checks(apk_file, list_scripts) -> None:
    ''' This function is responsible to check if the APK file exists and if the extension is .apk '''

    global args_list_scripts
    args_list_scripts = list_scripts

    file_name: str = apk_file
    check_if_file: bool = path.isfile(file_name)
    check_if_file_exists: bool = path.exists(file_name)
    check_extension: bool = file_name.endswith(".apk")

    if not(check_if_file or check_if_file_exists):
        print("[red][!] You have specified an invalid or non existent file or directory[/]")
        return True
    
    if not(check_extension):
        print("[red][!] File extension is not [b].apk[/], please check your file or input[/]")
        return True

    file_size: int = path.getsize(file_name)
    print(f"[black][-] Checking {file_name}. File size is [white]{file_size}[/][/]")

    extract_apk(file_name)


def extract_apk(file_name) -> None:
    ''' This function will create a folder called "apk-extracted" and extract the content from the apk file to that folder '''

    normal_dir_name: str = f"apk-extracted"
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

    check_app_dev_lang(normal_dir_name, apk_file)


def check_app_dev_lang(normal_dir_name, apk_file) -> None:
    ''' Detect the language that the app has been developed through shared object files  '''
    
    chdir(normal_dir_name)
    print(f"\n[black][-] Extracting APK classes...[/]")

    dvm = DalvikVMFormat(apk_file.get_dex())
    classes = dvm.get_classes()

    for apk_classes in classes:
        class_name = apk_classes.get_name()

        flutter_class = ['Lio/flutter/', 'Flutter']
        react_class = ['Lcom/facebook/react/', 'React']
        java_class = ['Landroidx/work/Worker', 'Java']
        supported_langs = [flutter_class, react_class, java_class]

        for default_classes in supported_langs:
            default_class_name = default_classes[0]
            app_lang = default_classes[1]

            if(default_class_name in class_name):
                print(f"[green][+] App is probably developed with [b]{app_lang}[/b][/]")
            
                if(args_list_scripts):
                    print(suggest_sslpinning(app_lang))
                return True
            else:
                pass

    print("\n[yellow][!] Done, exiting... [/]")
