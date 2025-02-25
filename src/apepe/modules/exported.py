from rich.console import Console
console = Console()

def exported(target) -> None:
    """
    Lists exported activities, services, receivers, and providers in the Android manifest.
    """

    manifest = target.get_android_manifest_xml()
    endpoints = ["activity", "service", "receiver", "provider"]

    for endpoint in endpoints:
        console.print(f"\n[green][+][/] App {endpoint}s", highlight=False)

        for element in manifest.findall(f".//{endpoint}"):
            name = element.get("{http://schemas.android.com/apk/res/android}name")
            exported = element.get("{http://schemas.android.com/apk/res/android}exported")

            if exported is None:
                has_intent_filter = element.find('.//intent-filter') is not None
                exported = 'True' if has_intent_filter else 'False'

            color = "green" if exported.lower() == 'true' else 'red'
            console.print(f'  \\_ {endpoint.capitalize()}: [yellow]{name}[/] - Exported: [{color}]{exported}[/]')