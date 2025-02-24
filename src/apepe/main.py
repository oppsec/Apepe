from rich.console import Console
console = Console()
from os import path, chdir
from pathlib import Path
from zipfile import ZipFile, BadZipFile
from shutil import rmtree

from androguard.core.apk import APK
from androguard.core.dex import DEX

from src.apepe.modules.suggest import suggest_sslpinning
from src.apepe.modules.deeplink import scraper
from src.apepe.modules.exported import exported

from loguru import logger
logger.remove(0)


def perform_checks(apk_file, list_scripts, deeplink) -> None:
    """
    This function is responsible to check if the APK file exists and
    if the extension is .apk
    """

    global args_list_scripts
    args_list_scripts = list_scripts

    global args_deeplink
    args_deeplink = deeplink

    file_name: str = apk_file
    check_if_file: bool = path.isfile(file_name)
    check_if_file_exists: bool = path.exists(file_name)
    check_extension: bool = file_name.endswith(".apk")

    if not(check_if_file or check_if_file_exists):
        console.print("[red][!][/] You have specified an invalid or non existent file or directory")
        return True
    
    if not(check_extension):
        console.print("[red][!][/] File extension is not [b].apk[/], please check your file or input")
        return True

    file_size: int = path.getsize(file_name)
    console.print(f"[yellow][!][/] Checking [yellow]{file_name}[/]. File size is [yellow]{file_size}[/] bytes", highlight=False)

    extract_apk(file_name)


def extract_apk(file_name) -> None:
    """
    This function will create a folder with the same name as of APK file and
    extract the content from the apk file to that folder 
    """

    normal_dir_name: str = f"{file_name.rstrip('.apk')}_extracted"
    current_dir = Path.cwd()
    target_dir = current_dir.joinpath(normal_dir_name)

    try:
        console.print(f"[yellow][!][/] Creating [yellow]{target_dir}[/] folder", highlight=False)

        if target_dir.exists():
            rmtree(target_dir)
        
        target_dir.mkdir(parents=True, exist_ok=True)

        console.print(f"[yellow][!][/] Extracting information from files on [yellow]{normal_dir_name}[/] folder", highlight=False)
        
        with ZipFile(file_name, mode="r") as archive:
            archive.extractall(path=normal_dir_name)

        apk_info_extraction(file_name, normal_dir_name)

    except FileNotFoundError:
        console.print(f"[red][!][/] APK file '{file_name}' not found.")
    
    except PermissionError:
        console.print(f"[red][!][/] Permission denied while creating '{target_dir}'.")

    except (OSError, BadZipFile) as error:
        console.print(f"[red][!][/] Error processing APK: {error}")

    

def apk_info_extraction(file_name, normal_dir_name) -> None:
    """
    Uses androguard's library functions to extract APK relevant information such as:
    Package Name, App Name, Activies, Permissions...
    """

    apk_file = APK(file_name)

    console.print("\n[green][+][/] App signature(s):", highlight=False)
    package_signature_V1 : bool = apk_file.is_signed_v1()
    package_signature_V3 : bool = apk_file.is_signed_v2()
    package_signature_V2 : bool = apk_file.is_signed_v3()
    console.print(f" \\_ V1: {package_signature_V1}\n \\_ V2: {package_signature_V2}\n \\_ V3: {package_signature_V3}")

    # Get app activities, services, providers and receivers
    exported(apk_file)

    # Get list of permissions used by the app
    try:
        app_permissions = apk_file.get_details_permissions()
        if len(app_permissions) != 0:
            console.print("\n[green][+][/] List of permissions:", highlight=False)

            for permission in app_permissions:
                console.print(f" \\_ {permission}")
        else:
            console.print("\n[red][!][/] No permission(s) found", highlight=False)
    except Exception as error:
        console.print(f"\n[red][!][/] Impossible to list permissions: {error}", highlight=False)
        pass

    # Get list of libraries used by the app
    try:
        app_libraries = apk_file.get_libraries()
        if len(app_libraries) != 0:
            console.print("\n[green][+][/] App libraries:", highlight=False)

            for library in app_libraries:
                console.print(f" \\_ {library}")
        else:
            console.print("\n[red][!][/] No libraries found", highlight=False)

    except Exception as error:
        console.print(f"\n[red][!][/] Impossible to list libraries: {error}", highlight=False)
        pass

    check_app_dev_lang(normal_dir_name, apk_file)


def check_app_dev_lang(normal_dir_name, apk_file) -> None:
    """
    Try to detect the app development language through classes name
    """
    
    chdir(normal_dir_name)
    console.print(f"\n[yellow][!][/] Extracting APK classes", highlight=False)

    try:
        dvm = DEX(apk_file.get_dex())
        classes = dvm.get_classes()

        lang_patterns = {
            'Lio/flutter/': 'Flutter',
            'Lcom/facebook/react/': 'React Native',
            'Landroidx/work/Worker': 'Java'
        }

        detected_lang = None

        for apk_class in classes:
            class_name = apk_class.get_name()

            for pattern, lang in lang_patterns.items():
                if pattern in class_name:
                    detected_lang = lang
                    break
            if detected_lang:
                break

        if detected_lang:
            console.print(f"[green][+][/] Development language detected: [b]{detected_lang}[/b]")
            if args_list_scripts:
                console.print(suggest_sslpinning(detected_lang))
        else:
            console.print("[red][!][/] Impossible to detect the app language")

    except Exception as error:
        console.print(f"[red][!][/] Error in [b]check_app_dev_lang[/b] function: {error}")
        return

    if args_deeplink:
        scraper(normal_dir_name, apk_file)

    console.print("\n[yellow][!][/] Finished!")