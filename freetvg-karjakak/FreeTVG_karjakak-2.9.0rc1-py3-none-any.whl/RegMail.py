import re
import webbrowser
from sys import platform
from textwrap import fill
from urllib import parse

__all__ = [""]


def composemail(sub: str, body: str):
    subject = f"[TVG]-{sub}"
    if platform.startswith("win"):
        webbrowser.open(f"mailto:?subject={subject}&body={parse.quote(body)}", new=1)
    else:
        webbrowser.open(f"mailto:?subject={subject}&body={body}", new=1)


def wrwords(text: str, wd: int, num: int):
    regex = re.compile(r"\s+")
    get = regex.match(text)
    if get:
        b = fill(text, wd, subsequent_indent=f'{" " * (get.span()[1]+num)}')
    else:
        b = fill(text, wd)
    return b
