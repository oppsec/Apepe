from rich import print

def get_banner() -> str:
    '''
    This function will return the main banner from the application
    '''

    banner = '''

   db    88""Yb 888888 88""Yb 888888 
  dPYb   88__dP 88__   88__dP 88__    - APK Analyzer by oppsec
 dP__Yb  88"""  88""   88"""  88""    - v1.0
dP""""Yb 88     888888 88     888888
    '''

    print(f"[bold yellow]{banner}[/]")