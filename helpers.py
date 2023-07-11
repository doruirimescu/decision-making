import textwrap


def wrap_text_to_80_chars(text: str, initial_indent=0, subsequent_indent=0) -> str:
    wrapper = textwrap.TextWrapper(width=80)
    wrapper.subsequent_indent = ' ' * subsequent_indent
    wrapper.initial_indent = ' ' * initial_indent
    return wrapper.fill(text)


def indent_n_chars(text: str, n: int) -> str:
    return textwrap.indent(text, ' ' * n)
