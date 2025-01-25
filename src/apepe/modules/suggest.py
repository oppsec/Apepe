URLS = [
    ['https://github.com/horangi-cyops/flutter-ssl-pinning-bypass', 'Flutter'],
    ['https://gist.github.com/owen800q/9c5ee9392f45dbcf44c5b434cdecf647', 'Flutter'],
    ['https://codeshare.frida.re/@vadim-a-yegorov/universalunpinner/', 'Java'],
    ['https://codeshare.frida.re/@vadim-a-yegorov/universalunpinner/', 'React'],
    ['https://codeshare.frida.re/@vadim-a-yegorov/universalunpinner/', 'Flutter'],
]

def suggest_sslpinning(lang: str) -> None:
    """
    Return URL value based in lang parameter which is returned by
    check_app_dev_lang function
    """

    for url in URLS:
        script_url: str = url[0]
        script_lang: str = url[1]

        if(lang == script_lang):
            return f'[green][+][/] SSL Pinning bypass recommended: {script_url}'