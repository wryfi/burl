####
burl
####

``burl`` (brief url) is a URL shortener written in python with the django framework.

As of version 2, this application and repo is for the standalone burl service,
providing a docker-packaged reference implementation of
`django-burl <https://gitlab.com/wryfi/django-burl>`__. If you're looking for a
URL-shortener to include in your own django project, *see*
`django-burl <https://gitlab.com/wryfi/django-burl>`__.

Features include:

* data models and REST API from
  `django-burl <https://gitlab.com/wryfi/django-burl>`__
* JWT authentication
* CORS management via `django-cors-headers <https://github.com/adamchainz/django-cors-headers>`__
* swagger-ui
* user model with ``UUIDField`` for its primary key
* account management pages/templates
* static assets served via `whitenoise <https://whitenoise.evans.io/en/stable/>`__
* `gunicorn <https://gunicorn.org/>`__ WSGI server
* easy configuration with `cfitall <https://github.com/wryfi/cfitall>`__

Quick Start
===========

First, configure a postgres user and database to host ``burl``'s data, then create
a file ``/etc/burl/env`` specifing the environment variables for configuring
``burl`` (see below).

Run the latest image from docker hub (remember to change 10.0.0.10 to
the ip of the postgres server you configured above)::

    docker pull wryfi/burl:latest
    docker run -dit --name=myburl -p 8000:8000 --env-file /etc/burl/env \
        --add-host=dbhost:10.0.0.10 \
        --restart unless-stopped wryfi/burl:latest run
    docker exec -it myburl burl-manager createsuperuser
    docker exec -it myburl burl-manager set_default_site --name localhost --domain localhost

Point your browser to http://localhost:8000/admin and create some BURLs!

Or go old school::

    curl \
      -X POST -H "Content-Type: application/json" \
      -d '{"username": "dooper", "password": "sooperuser"}' \
      http://localhost:8000/api/v2/token/auth
    ...
    {
      "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU",
      "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"
    }

    curl \
      -X POST -H "Content-Type: application/json" \
      -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU" \
      -d '{"url": "https://archive.org", "burl": "arc"}' \
      http://localhost:8000/api/v2/burls/
    ...
    {
      "burl": "arc",
      "created": "2022-03-14T16:16:09.353538-05:00",
      "description": "",
      "enabled": true,
      "updated": "2022-03-14T16:16:09.353543-05:00",
      "url": "https://archive.org",
      "user": "aec88b92-267f-430e-b4e2-0c63f4fc411a"
    }

    curl -IL "http://localhost:8000/arc/"
    ...
    HTTP/1.0 302 Found
    Content-Type: text/html; charset=utf-8
    Location: https://archive.org
    X-Frame-Options: DENY
    Content-Length: 0
    X-Content-Type-Options: nosniff
    Referrer-Policy: same-origin
    Cross-Origin-Opener-Policy: same-origin
    Vary: Origin
    Server: Werkzeug/2.0.3 Python/3.10.2
    Date: Mon, 14 Mar 2022 21:21:03 GMT

    HTTP/1.1 200 OK
    Server: nginx/1.18.0 (Ubuntu)
    Date: Mon, 14 Mar 2022 21:21:04 GMT
    Content-Type: text/html; charset=utf-8
    Connection: close
    vary: Accept-Encoding
    Strict-Transport-Security: max-age=15724800
    Cache-Control: no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0

Configuration
=============

``burl`` uses `cfitall <https://gitlab.com/wryfi/cfitall>`__ for managing its
most commonly configured settings. It will search ``/etc/burl`` and then
``~/.local/etc/burl`` for a ``burl.yml`` or ``burl.json`` settings file, and/or
read its configuration from a series of environment variables.

Example yaml file: ::

    admin:
      rough_count_min: 1000
    api:
      page_size: 25
    app:
      burl_blacklist:
      - admin
      - api
      - static
      - media
      debug: false
      default_redirect_url: https://www.wikipedia.org/
      hashid_alphabet: abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ0123456789
      media_root: /Users/burl/.local/var/burl/media
      static_root: /Users/burl/.local/share/burl/static
      time_zone: America/Los_Angeles
    db:
      default:
        engine: django.db.backends.postgresql_psycopg2
        host: 127.0.0.1
        name: burl
        password: burl
        port: 5432
        user: burl
    http:
      secure_proxy_ssl_header_name: HTTP_X_FORWARDED_PROTO
      secure_proxy_ssl_header_value: http
      use_x_forwarded_hosts: true
    logging:
      app:
        level: warn
      burl:
        level: info
      log_dir: /Users/burl/.local/var/log/burl
    mail:
      default_from_email: nobody@burl.test
      sendgrid_api_key: ''
    security:
      allowed_hosts:
      - localhost
      - 127.0.0.1
      cors:
        allow_all_origins: false
        allowed_origin_regexes: []
        allowed_origins: []
      jwt:
        access_lifetime: 600
        refresh_lifetime: 86400
      secret_key: jeirainooyieShaequeeng8av9gah6geiv1ooTh6quoo9meireeRayoo6un7xah
      sendgrid_api_key: ''

Corresponding environment variables: ::

    BURL__ADMIN__ROUGH_COUNT_MIN
    BURL__API__PAGE_SIZE
    BURL__APP__BURL_BLACKLIST
    BURL__APP__DEBUG
    BURL__APP__DEFAULT_REDIRECT_URL
    BURL__APP__HASHID_ALPHABET
    BURL__APP__MEDIA_ROOT
    BURL__APP__STATIC_ROOT
    BURL__APP__TIME_ZONE
    BURL__DB__DEFAULT__ENGINE
    BURL__DB__DEFAULT__HOST
    BURL__DB__DEFAULT__NAME
    BURL__DB__DEFAULT__PASSWORD
    BURL__DB__DEFAULT__PORT
    BURL__DB__DEFAULT__USER
    BURL__HTTP__SECURE_PROXY_SSL_HEADER_NAME
    BURL__HTTP__SECURE_PROXY_SSL_HEADER_VALUE
    BURL__HTTP__USE_X_FORWARDED_HOST
    BURL__LOGGING__APP__LEVEL
    BURL__LOGGING__BURL__LEVEL
    BURL__LOGGING__LOG_DIR
    BURL__MAIL__DEFAULT_FROM_EMAIL
    BURL__MAIL__SENDGRID_API_KEY
    BURL__SECURITY__ALLOWED_HOSTS
    BURL__SECURITY__CORS__ALLOWED_ORIGINS
    BURL__SECURITY__CORS__ALLOWED_ORIGIN_REGEXES
    BURL__SECURITY__CORS__ALLOW_ALL_ORIGINS
    BURL__SECURITY__JWT__ACCESS_LIFETIME
    BURL__SECURITY__JWT__REFRESH_LIFETIME
    BURL__SECURITY__SECRET_KEY
    BURL__SECURITY__SENDGRID_API_KEY

Of course, per the django convention, you can always set the
``DJANGO_SETTINGS_MODULE`` environment variable to a python module of your
choice, to further extend or bypass all of ``burl``'s settings and configuration
mechanisms if needed.

Configuration Notes
-------------------

Email
~~~~~

If you want working email (e.g. for password resets) the only supported option
at this time is to use sendgrid.  Set the ``security.sendgrid_api_key`` setting
(``BURL__SECURITY__SENDGRID_API_KEY`` environment variable) to enable sendgrid
support. Otherwise all email is printed to the console and never sent.


Development
===========

Implementation
--------------

``burl`` is a reference implementation of
`django-burl <https://gitlab.com/wryfi/django-burl>`__, which implements most
of the functionality found in ``burl``. Please review django-burl's documentation
for details.

``burl`` adds JWT authentication to django-burl via
`Simple JWT <https://django-rest-framework-simplejwt.readthedocs.io/en/latest/>`__.

The current Swagger UI (api documentation) can be found at ``/api/v2/swagger``
of the running service.

The django admin can be found as usual at ``/admin``.

code requirements
-----------------

``burl`` requires python 3.7 or newer.  Python 2 is not supported.

``burl`` should run anywhere python will run, most easily on a unix-like system.


database requirements
---------------------

``burl`` strongly recommends using a postgresql database via python's
``psycopg2`` library.

You will need a C compiler, python header files, and postgres development
libraries on your system to build the postgres ``psycopg2`` module needed
for postgresql.


Installation
------------

``burl`` is made to be installed via the standard python installation methods.
You can install it as simply as running::

    pip install burl

It is recommended, however, that you install ``burl`` in a virtualenv or
Docker container. For development, in particular, the easiest way to set
everything up is to use ``pipenv`` (see below).

Once you have installed ``burl``, you will need to create a database for its
use. The default configuration expects a database called ``burl``, owned by
a user named ``burl``, with a password of ``burl``. You should alter these
settings by using the configuration mechanisms described above.

Once your database is configured, run the database migrations to create::

    burl-manager migrate

Then create a new superuser::

    burl-manager createsuperuser

Now you should be ready to run ``burl``!  You can run a test/development server
by running ``burl-manager runserver`` to ensure that everything is working. In
production, you should deploy behind a WSGI server.

Deployment
----------

``burl`` is a straightforward django app, with nothing fancy.

You can deploy burl with any WSGI-compliant web server. Running
`gunicorn <http://gunicorn.org/>`_ as the backend WSGI server, with an nginx
reverse proxy in front of it, is a common and well-supported configuration.

`Deploying Django <https://docs.djangoproject.com/en/2.0/howto/deployment/>`_
has some generic information about deploying django applications that you may
find useful if you are new to this stack.

Docker
------

The included Dockerfile builds a container that bundles burl with gunicorn and
exposes gunicorn on port 8000.  It builds with uid ``65432`` by default, which
you can change on the ``docker build`` command line, e.g.::

    docker build --build-arg uid=23456 -t burl .

This container does not include postgres or nginx. You will need postgres to run
burl, and you will want to put nginx in front of the container.

Once you have a built container, it can be activated as follows::

    docker run -dit -p 8000:8000 --env-file /etc/burl/env --add-host=dbhost:10.0.0.10 \
        --restart unless-stopped burl:latest burl


Tooling
-------

``burl`` uses a modern python toolchain, consisting of:

- `pipenv <https://docs.pipenv.org/>`_ for managing dependencies,
- `pbr <https://docs.openstack.org/pbr/latest/>`_ build system,
- docker support,
- semantic version numbers,
- git flow branching scheme.

To start coding, first install ``pipenv``, then clone this repo and run
``pipenv install -d``. This will set up a virtualenv, install all of
the dependencies, and install burl in editable mode. You should now be
able to run commands like ``pipenv shell``, ``pipenv run burl-manager test``,
etc.

When using ``pipenv`` you can make use of a ``.env`` file in the source root,
and set the requisite environment variables (above) there. This file is
ignored in ``.gitignore`` and local to your environment.

*See:*

- `Why Python devs should use Pipenv <https://opensource.com/article/18/2/why-python-devs-should-use-pipenv>`_

Tests
-----

``burl`` was not developed using TDD, but has reasonable test coverage.
Tests are located in the standard places for django applications. New PRs
should include relevant tests whenever possible.
