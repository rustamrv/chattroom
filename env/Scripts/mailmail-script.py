#!d:\project\chattroom\env\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'Twisted==20.3.0','console_scripts','mailmail'
__requires__ = 'Twisted==20.3.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('Twisted==20.3.0', 'console_scripts', 'mailmail')()
    )
