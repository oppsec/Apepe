from rich.console import Console
console = Console()

def get_banner() -> str:
    '''
    This function will return the main banner from the application
    '''

    banner = '''
 _____           
|  _  |___ ___ ___ ___ 
|     | . | -_| . | -_| - APK Analyzer v1.3
|__|__|  _|___|  _|___|   by @oppsec
      |_|     |_|      
    '''

    console.print(f"[bright_white]{banner}[/]", highlight=False)