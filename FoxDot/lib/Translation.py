"""Translation (t9n) module.

Examples
--------
Create .pot file Portable Object Template:
  $ xgettext --from-code=UTF-8 -o FoxDot.pot -k'_' -l python FoxDot/lib/Workspace/*.py  # extract new phrases

Add new locale:
  $ FOXDOT_LOCALE='pt_BR'  # 'en_GB', 'es_CO' or just 'ru', 'fr'
  $ msginit -i FoxDot.pot -o FoxDot/locale/$FOXDOT_LOCALE/LC_MESSAGES/FoxDot.po --locale $FOXDOT_LOCALE

Add new phrases to existing locale files:
  $ msgmerge -U FoxDot/locale/$FOXDOT_LOCALE/LC_MESSAGES/FoxDot.po FoxDot.pot

Create/Update .mo file:
  $ msgfmt -o FoxDot/locale/$FOXDOT_LOCALE/LC_MESSAGES/FoxDot.mo FoxDot/locale/$FOXDOT_LOCALE/LC_MESSAGES/FoxDot.po
"""
from gettext import translation

from .Settings import FOXDOT_LOCALE_DIR, GET_LANG

t = translation('FoxDot', FOXDOT_LOCALE_DIR, [GET_LANG()], fallback=True)
# t.install()
_ = t.gettext
