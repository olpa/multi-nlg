import typing


def generate(interlingua: str) -> typing.Mapping[str, str]:
    if 'nerkla' in interlingua:
        return {
                'en': 'John broke into the room.',
                'es': 'Juan forzó la entrada al cuarto.',
                'de': 'Johann brach ins Zimmer ein.',
                'ru': 'Джон ворвался в комнату.',
                'zh': '约翰闯进房间。',
                }
    if 'dakfu' in interlingua:
        return {
                'en': 'I stabbed John.',
                'es': 'Yo le di puñaladas a Juan.',
                'de': 'Ich erstach Johann.',
                'ru': 'Я ударил Джона ножом.',
                'zh': '我刺伤了约翰。',
                }
    pass
