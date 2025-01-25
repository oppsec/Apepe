urls = [
    ['https://github.com/horangi-cyops/flutter-ssl-pinning-bypass', 'Flutter'],
    ['https://gist.github.com/owen800q/9c5ee9392f45dbcf44c5b434cdecf647', 'Flutter'],
    ['https://codeshare.frida.re/@vadim-a-yegorov/universalunpinner/', 'Java'],
    ['https://codeshare.frida.re/@vadim-a-yegorov/universalunpinner/', 'React'],
    ['https://codeshare.frida.re/@vadim-a-yegorov/universalunpinner/', 'Flutter'],
]

def suggest_sslpinning(lang) -> str:
    ''' This function will pass through the urls array values and return they '''

    for url in urls:
        script_url: str = url[0]
        script_lang: str = url[1]

        if(lang == script_lang):
            return f'[yellow][i]* SSL pinning script recommend: [u]{script_url}[/i][/u][/]'