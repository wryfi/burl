import os
from django.core.exceptions import ImproperlyConfigured


def get_env(variable):
    try:
        return os.environ[variable]
    except KeyError:
        message = 'Invalid settings. Please set the {} environment variable'.format(variable)
        raise ImproperlyConfigured(message)


def get_log_dir():
    log_dir = None
    if os.access('/var/log/hashurl', os.W_OK):
        log_dir = '/var/log/hashurl'
    elif 'HOME' in os.environ and os.access(os.path.join(os.environ['HOME'], 'var', 'log'), os.W_OK):
        log_dir = os.path.join(os.environ['HOME'], 'var', 'log')
    elif 'HOME' in os.environ:
        log_dir = os.environ['HOME']
    elif os.path.isdir('/tmp') and os.access('/tmp', os.W_OK):
        log_dir = '/tmp'
    return log_dir
