_vowels = set('aeiouy')


def to_english_piglatin(text: str) -> str:
    translated = []
    for word in text.split():
        prefix = []
        for i, ch in enumerate(word):
            if ch.isalpha():
                word = word[i:]
                break
            else:
                prefix.append(ch)

        suffix = []
        for i, ch in enumerate(word):
            if not ch.isalpha():
                word = word[:i]
                break
            suffix = word[i + 1:]

        was_upper = word.isupper()
        was_title = word.istitle()
        word = word.lower()

        consonants = []
        while len(word) and not word[0] in _vowels:
            consonants.append(word[0])
            word = word[1:]

        if consonants:
            word += ''.join(consonants) + 'ay'
        else:
            word += 'yay'

        if was_upper:
            word = word.upper()

        if was_title:
            word = word.title()

        translated.append(''.join(prefix + [word] + list(suffix)))

    return ' '.join(translated)
