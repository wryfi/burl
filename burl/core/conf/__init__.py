import os

from cfitall.config import ConfigManager
from burl.core import utils

home = os.environ.get("HOME")

config = ConfigManager("burl")

config.set_default("admin.rough_count_min", 1000)

config.set_default("api.page_size", 20)

config.set_default("app.burl_blacklist", ["admin", "api", "static", "media"])
config.set_default("app.debug", False)
config.set_default("app.default_redirect_url", "https://www.wikipedia.org/")
config.set_default(
    "app.hashid_alphabet", "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ0123456789"
)
config.set_default(
    "app.media_root", os.path.join(home, ".local", "var", "burl", "media")
)
config.set_default("app.time_zone", "America/Los_Angeles")
config.set_default(
    "app.static_root", os.path.join(home, ".local", "share", "burl", "static")
)

config.set_default("db.default.name", "burl")
config.set_default("db.default.user", "burl")
config.set_default("db.default.password", "burl")
config.set_default("db.default.host", "127.0.0.1")
config.set_default("db.default.port", 5432)
config.set_default("db.default.engine", "django.db.backends.postgresql_psycopg2")

config.set_default("logging.app.level", "INFO")
config.set_default("logging.burl.level", "WARNING")
config.set_default("logging.log_dir", utils.get_log_dir())

config.set_default("security.allowed_hosts", ["*"])
config.set_default("security.cors.allowed_origins", [])
config.set_default("security.cors.allowed_origin_regexes", [])
config.set_default("security.cors.allow_all_origins", False)
config.set_default("security.jwt.access_lifetime", 600)
config.set_default("security.jwt.refresh_lifetime", 86400)
config.set_default(
    "security.secret_key",
    "xFLJ3AXXTpS5eODotsmxkzCOVIHmK7JZggV55YQjgWqKko7nGaLBJcwSfYVBP9JjfJjyZ",
)
config.set_default("security.sendgrid_api_key", "")

config.add_config_path("/etc/burl")
config.add_config_path(os.path.join(home, ".local", "etc", "burl"))
config.read_config()
