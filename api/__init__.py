import glob
import json
import typing

from fastapi import Request
from fastapi.templating import Jinja2Templates

from settings import (
    LANGUAGE,
)  # We can configure this based on locale headers or user locale


# Templates config
def flash(request: Request, message: typing.Any, category: str = "primary") -> None:
    if "_messages" not in request.session:
        request.session["_messages"] = []
        request.session["_messages"].append({"message": message, "category": category})


def get_flashed_messages(request: Request):
    return request.session.pop("_messages") if "_messages" in request.session else []


templates = Jinja2Templates(directory="client/templates")
templates.env.globals["get_flashed_messages"] = get_flashed_messages

# i18n config
_translations = {}

language_list = glob.glob("api/languages/*.json")
for language in language_list:
    filename = language.split("/")[2]
    lang_code = filename[:2]
    with open(language, "r", encoding="utf8") as file:
        _translations[lang_code] = json.load(file)

global _l
_l = _translations.get(LANGUAGE, {})
