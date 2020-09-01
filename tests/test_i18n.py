"""
test i18n .po is updated
test i18n .po files don't contain untranslated strings
"""
import os
import pathlib

import polib


# I18N_PATH = f"{(pathlib.Path().absolute())}/../app/i18n"
#
#
# def test_lc_messages_translated():
#     all_dirs = [d for d in os.listdir(I18N_PATH) if os.path.isdir(f"{I18N_PATH}/{d}")]
#
#     for lang in all_dirs:
#         po = polib.pofile(f'{I18N_PATH}/{lang}/LC_MESSAGES/messages.po')
#         for entry in po:
#             assert entry.msgstr != '', f'"{entry.msgid}" not translated in {lang}'
#
#     print("All entries are translated")
