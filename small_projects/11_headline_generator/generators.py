import random

NOUNS = ('Athlete,Shovel,Clown,Paleo Diet,Doctor,Parent,Cat,Dog,Chicken,Robot,Video Game,Avocado,'
         'Plastic Straw,Serial Killer,Computer,Telephone Psychic,Telephone').split(',')
MODES = 'Soon,This Year,Later Today,Right Now,Next Week'.split(',')
OBJECT_PRONOUNS = 'Her,Him,Them'.split(',')
COUNTRIES = ('France,United Kingdom,Germany,Italy,Portugal,Estonia,Finland,Sweden,Norway,'
             'Belgium,Spain,Bulgaria,Russia,Poland,Switzerland,Madagascar,Kongo,Ethiopia,San Marino,'
             'Malta,Israel,Slovakia,Croatia,Romania,Luxembourg,Latvia,Armenia,Turkey').split(',')
PLACES = ('House,Attic,Bank Deposit Box,Pocket,School,Basement,Workplace,'
          'Donut Shop,Wardrobe,Bunker,Shelter,Car,Van,Drawer').split(',')


def are_millenials_killing() -> str:
    noun = random.choice(NOUNS)
    return f'Are Millenials Killing the {noun} Industry?'


def what_you_dont_know() -> str:
    noun = random.choice(NOUNS)
    plural_noun = random.choice(NOUNS) + 's'
    mode = random.choice(MODES)
    return f'Without This {noun}, {plural_noun} Could Kill You {mode}'


def big_companies_hate_her() -> str:
    pronoun = random.choice('Her Him Them'.split())
    country = random.choice(COUNTRIES)
    subject = random.choice(NOUNS)
    object_ = random.choice(NOUNS)
    return f'Big Companies Hate {pronoun}! See How This {subject} From {country} Invented a Cheaper {object_}'


def you_wont_believe() -> str:
    country = random.choice(COUNTRIES)
    noun = random.choice(NOUNS)
    pronoun = random.choice('His Her'.split())
    place = random.choice(PLACES)
    return f"You Won't Believe What This {noun} From {country} Found in {pronoun} {place}"


def dont_want_you_to_know() -> str:
    first = random.choice(NOUNS)
    second = random.choice(NOUNS)
    return f"What {first}s Don't Want You To Know About {second}s"


def gift_idea() -> str:
    number = random.randint(7, 15)
    country = random.choice(COUNTRIES)
    noun = random.choice(NOUNS)
    return f'{number} Gift Ideas to Give Your {noun} From {country}'


def reasons_why() -> str:
    num_reasons = random.randint(3, 19)
    index = random.randint(1, num_reasons)
    noun = random.choice(NOUNS)
    return (
        f'{num_reasons} Reasons Why {noun}s Are More Interesting '
        f'Then You Think (Number {index} Will Surprise You!)'
    )


def job_automated_headline() -> str:
    country = random.choice(COUNTRIES)
    noun = random.choice(NOUNS)

    index = random.randint(0, 2)
    possessive_pronoun = 'Her His Their'.split()[index]
    personal_pronoun = 'She He They'.split()[index]

    verb = 'Were' if possessive_pronoun == 'Their' else 'Was'

    return (
        f"This {country} {noun} Didn't Think Robots Would Take {possessive_pronoun} Job. "
        f"{personal_pronoun} {verb} Wrong."
    )
