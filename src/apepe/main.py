from rich import print
from rich.console import Console
console = Console()
from os import path, mkdir, chdir
from pathlib import Path
from zipfile import ZipFile

from androguard.core.apk import APK
from androguard.core.dex import DEX

from src.apepe.modules.suggest import suggest_sslpinning
from src.apepe.modules.deeplink import scraper

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

    normal_dir_name: str = f"{file_name.rstrip('.apk')}_results"
    current_dir = Path.cwd()

    console.print(f"[yellow][!][/] Creating [yellow]{normal_dir_name}[/] folder to extract the apk", highlight=False)

    if not(current_dir.joinpath(normal_dir_name).exists()):
        Path(normal_dir_name).mkdir(parents=True, exist_ok=True)
        console.print(f"[green][+][/] Created [yellow]{normal_dir_name}[/] folder", highlight=False)

        with ZipFile(file_name, mode="r") as archive:
            archive.extractall(path=normal_dir_name)

        console.print(f"[yellow][!][/] Extracting information from files on [yellow]{normal_dir_name}[/] folder", highlight=False)
        apk_info_extraction(file_name, normal_dir_name)

    else:
        console.print(f"[red][!][/] You already have an [b]{normal_dir_name}[/] folder on this directory, delete or move to another place")
        return True
    

def apk_info_extraction(file_name, normal_dir_name) -> None:
    """
    Uses androguard's library functions to extract APK relevant information such as:
    Package Name, App Name, Activies, Permissions...
    """

    apk_file = APK(file_name)

    # Get APK package name, app name, package signature and if it's signed
    package_name = apk_file.get_package()

    try:
        app_name = apk_file.get_app_name()
    except:
        app_name = package_name

    package_signature: str = apk_file.get_signature_name()
    package_signature_V1 : bool = apk_file.is_signed()
    package_signature_V3 : bool = apk_file.is_signed_v2()
    package_signature_V2 : bool = apk_file.is_signed_v3()

    console.print("\n[[green]+[/]] APK Standard Information:")

    console.print(f'''[green] \\_ Package Name: [white]{package_name}[/white]
 \\_ App Name: [white]{app_name}[/white]
 \\_ Is App Signed: [white]{package_signature_V1}[/white]
    |_ Signature Version 1: [white]{package_signature_V1}[/white]
    |_ Signature Version 2: [white]{package_signature_V2}[/white]
    |_ Signature Version 3: [white]{package_signature_V3}[/white]
 \\_ Package Signature: [white]{package_signature}[/white]
    [/]''', highlight=False)


    # Get APK Activies
    app_activies = apk_file.get_activities()
    if len(app_activies) != 0:
        console.print("[green][+][/] List of activities:")

        main_activity = apk_file.get_main_activity()
        console.print(f" \\_ [green]* Main Activity[/]: {main_activity}")

        for activity_name in app_activies:
            console.print(f"  \\_ {activity_name}")
    else:
        console.print("[red][!][/] No activies found")

    # Get APK Permissions
    try:
        app_permissions = apk_file.get_details_permissions()
        if len(app_permissions) != 0:
            console.print("\n[green][+][/] List of permission(s):", highlight=False)

            for permission in app_permissions:
                console.print(f" \\_ {permission}")
        else:
            console.print("\n[red][!][/] No permission(s) found", highlight=False)
    except:
        pass

    # Get APK Libraries
    app_libraries = apk_file.get_libraries()
    if len(app_libraries) != 0:
        console.print("\n[green][+][/] List of librarie(s):", highlight=False)

        for library in app_libraries:
            console.print(f" \\_ {library}")
    else:
        console.print("\n[red][!][/] No librarie(s) found", highlight=False)

    # Get APK Services
    app_services = apk_file.get_services()
    if len(app_services) != 0:
        console.print("\n[green][+][/] List of service(s):", highlight=False)

        for service in app_services:
            console.print(f" \\_ {service}")
    else:
        console.print("\n[red][!][/] No service(s) found", highlight=False)

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
                    console.print(f"[green][+][/] App is probably developed with [b]{app_lang}[/b]")
                
                    if(args_list_scripts):
                        console.print(suggest_sslpinning(app_lang))
                    
                    if(args_deeplink):
                        scraper(normal_dir_name, apk_file)

                    return True
                
                else:
                    pass

    except Exception as error:
        console.print(f"[red][!][/] Error in [b]check_app_dev_lang[/] function: {error}")
        return

    console.print("[yellow][!][/] Finished!")
