import os
from django.core.exceptions import ImproperlyConfigured


def get_env(setting, fallback=None):
    try:
        return os.environ[setting]
    except KeyError:
        if fallback:
            return fallback
        else:
            return ImproperlyConfigured(
                "Please set the {} environment variable".format(setting)
            )


def get_log_dir():
    if "HOME" in os.environ:
        home = os.environ["HOME"]
        try_dirs = [
            "/var/log/burl",
            os.path.join(home, ".local", "var", "log", "burl"),
            home,
            "/tmp/burl",
            "/tmp",
        ]
    else:
        try_dirs = ["/var/log/burl", "/tmp/burl", "/tmp"]
    for log_dir in try_dirs:
        if os.path.isdir(log_dir):
            if os.access(log_dir, os.W_OK):
                return log_dir
            elif os.access(os.path.dirname(log_dir), os.W_OK):
                try:
                    os.makedirs(log_dir)
                    return log_dir
                except:
                    continue
