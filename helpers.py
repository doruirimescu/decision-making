import textwrap


def wrap_text_to_80_chars(text: str) -> str:
    return textwrap.fill(text, width=80)


def indent_n_chars(text: str, n: int) -> str:
    return textwrap.indent(text, ' ' * n)
