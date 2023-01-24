import glob
import json
from functools import wraps

from fastapi.templating import Jinja2Templates

# Templates config
templates = Jinja2Templates(directory="client/templates")

# i18n config
_translations = {}
default_locale = "en"  # We can configure this based on locale headers or user locale

language_list = glob.glob("api/languages/*.json")
for language in language_list:
    filename = language.split("/")[2]
    lang_code = filename[:2]
    with open(language, "r", encoding="utf8") as file:
        _translations[lang_code] = json.load(file)

global _l
_l = _translations.get(default_locale, {})
