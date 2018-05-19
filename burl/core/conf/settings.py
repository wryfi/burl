import os
from importlib.machinery import SourceFileLoader
import sys

from burl.core.conf import defaults

# override settings from the first configuration file we find
home = os.environ.get('HOME', '/tmp')
config_dirs = ['/etc/burl', os.path.join(home, '.config', 'burl'), os.path.join(home, 'etc', 'burl')]
for config_dir in config_dirs:
    config_file = os.path.join(config_dir, 'burlrc')
    if os.path.isfile(config_file):
        local_settings = SourceFileLoader('local_settings', config_file).load_module()
        for attr in dir(local_settings):
            if attr.isupper():
                setattr(defaults, attr, getattr(local_settings, attr))
        break

module = sys.modules[__name__]

for setting in dir(defaults):
    if setting.isupper():
        setattr(module, setting, getattr(defaults, setting))
