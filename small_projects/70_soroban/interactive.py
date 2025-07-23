from pyparsing import ParseResults, Combine, one_of, Word, nums, ParseException, Optional

sign = one_of("+ -")
number = Combine(Optional(sign) + Word(nums)).set_parse_action(lambda t: int(t[0]))
keyword = one_of("null quit", caseless=True, as_keyword=True)
action = number | keyword


def ask_player(prompt: str) -> ParseResults | None:
    print(prompt)
    answer = None
    try:
        while not answer:
            answer = input("> ").strip()
        result = action.parse_string(answer, parse_all=True)
    except ParseException:
        result = None
    except KeyboardInterrupt:
        exit()
    return result
