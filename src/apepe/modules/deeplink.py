import json
import re

from rich.console import Console
console = Console()
from pathlib import Path

from androguard.core.dex import DEX
from androguard.core.apk import APK

from lxml.etree import tostring

DEEPLINK_PATTERN = r'\b\w+://[^\s]+'


def dex_handler(file_path: Path) -> list:
    """
    Extract readable strings from a .dex file and filter for deeplinks,
    excluding those that start with 'http://', 'https://' or 'parse'
    """
    results = []

    try:
        with file_path.open('rb') as dex_file:
            content = DEX(dex_file.read())
            strings = content.get_strings()
            results = [
                s for s in strings 
                if isinstance(s, str) 
                and re.search(DEEPLINK_PATTERN, s) 
                and not ('http://' in s or 'https://' in s or 'parse' in s)
            ]

    except Exception as error:
        console.print(f"[red][!][/] Failed to read DEX file [yellow]{file_path}[/]: {error}")
        return []

    if len(results) == 0:
        return f"[red][!][/] No deeplinks found in [yellow]{file_path}[/]\n"
    else:   
        return "\n".join(results) + "\n"


def json_handler(file_path: Path) -> list:
    """
    Extract readable strings from a .json file and filter for deeplinks,
    excluding those that start with 'http://' or 'https://'.
    """
    results = []

    try:
        with file_path.open('r', encoding='utf-8') as json_file:
            content = json.load(json_file)
            stack = [content]

            while stack:
                obj = stack.pop()
                if isinstance(obj, dict):
                    stack.extend(obj.values())
                elif isinstance(obj, list):
                    stack.extend(obj)
                elif isinstance(obj, str):
                    if re.search(DEEPLINK_PATTERN, obj) and not ('http://' in obj or 'https://' in obj or 'parse' in obj):
                        results.append(obj)

    except Exception as error:
        console.print(f"[red][!][/] Failed to read JSON file [yellow]{file_path}[/]: {error}")
        return []
    
    if len(results) == 0:
        return f"[red][!][/] No deeplinks found in [yellow]{file_path}[/]\n"
    else:   
        return "\n".join(results) + "\n"
    

def android_manifest_handler(apk_file: str) -> None:
    """
    Extract readable intent-filter (scheme, host and path) from AndroidManifest.xml
    """

    console.print("[green][+][/] AndroidManifest.xml:")
    results = []

    seen = set()

    try:
        manifest = APK.get_android_manifest_xml(apk_file)
        manifest_content: str = tostring(manifest, pretty_print=True, encoding="unicode")
        
        if len(manifest_content) == 0:
            console.print(f"[red][!][/] AndroidManifest.xml content is 0 - [yellow]{apk_file}[/]")

        else:
            for intent_filter in manifest.findall(".//intent-filter"):
                data_tag = intent_filter.find("data")

                if data_tag is not None:
                    scheme = data_tag.get("{http://schemas.android.com/apk/res/android}scheme", "")
                    host = data_tag.get("{http://schemas.android.com/apk/res/android}host", "")
                    path = data_tag.get("{http://schemas.android.com/apk/res/android}path", "")

                    formatted_url = f"{scheme}://{host}{path}" if scheme and host and path else f"{scheme}://{host}"
                    if formatted_url not in seen:
                        results.append(formatted_url)

        if len(results) == 0:
            return f"[red][!][/] No results for [yellow]{apk_file}[/]\n"
        else:   
            return "\n".join(results) + "\n"

    except Exception as error:
        console.print(f"[red][!][/] Failed to read AndroidManifest.xml file [yellow]{apk_file}[/]: {error}")
        return []


def scraper(extraction_path: str, apk_file: str) -> None:
    """
    This module aims to get all the readable strings from the extracted files (JSON and DEX)
    and search for possible deeplinks.

    extraction_path: Path to the extracted content directory
    """
    console.print(f"\n[yellow][!][/] Searching for [yellow]deeplinks[/] [yellow]({extraction_path}[/])")
    path = Path(extraction_path)

    # Get the results variable content and print the result
    console.print(android_manifest_handler(apk_file), highlight=False)

    extensions = ['.dex', '.json']
    for extension in extensions:
        
        file_paths = path.glob(f'**/*{extension}')

        for file_path in file_paths:
            file_path_str = str(file_path)
            console.print(f"[yellow][!][/] Checking file: [yellow]{file_path_str}[/]")

            if(extension == '.dex'):
                console.print(dex_handler(file_path), highlight=False)

            if(extension == '.json'):
                console.print(json_handler(file_path), highlight=False)