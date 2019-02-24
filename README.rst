####
burl
####

``burl`` (brief url) is a URL shortener written in Django. It has a simple REST
API, allowing it to integrate seamlessly as a microservice in many
application architectures.


Implementation
==============

``burl`` implements a URL shortening service by allowing authenticated users
to create a brief URL pointing to any other URL.  When the brief URL is
requested from ``burl``, it returns a redirect to the original URL.

There is a minimal restful API implemented with django rest framework.
The current version can be found at ``/api/v1`` or you can view the
swagger interface at ``/api/v1/swagger``.  Note that you will need to
authenticate to view the relevant api endpoints. Session and
token based authentication are enabled by default.

``burl`` uses `hashids <https://hashids.org/>`_ for automatically generated
brief URLs. Each auto-generated BURL is created using a random salt and a
random number passed into the hashids library. This value is then stored in the
database. The random BURLs generated in this manner should be sufficiently
difficult to reverse engineer.


Requirements
============

code
----

``burl`` is written in python 3 with django 2.1.  It will probably run fine
on python 3.4+ but is developed on python 3.7. Python 2 is not supported.
``burl`` should run anywhere python will run, most easily on a unix-like system.


database
--------

``burl`` requires a relational database.  Technically, any of the databases
supported by django should work, but officially only postgres is supported.

You will need database development libraries on your system to build the postgres
``psycopg2`` module needed for postgresql.

Installation
============

``burl`` is made to be installed via the standard python installation methods.
You can install it as simply as running::

    pip install burl

It is recommended, however, that you install ``burl`` in a virtualenv or
Docker container. For development, in particular, the easiest way to set
everything up is to use ``pipenv`` (see below).

Once you have installed ``burl``, you will need to create a database for its
use. The default configuration expects a database called ``burl``, owned by
a user named ``burl``, with a password specified in the environment variable
``$BURL_POSTGRES_PASSWORD``. You can alter these settings by overriding
the django ``DATABASES`` configuration dictionary in your ``burlrc`` (see
below).

Once your database is configured, run the database migrations to create
the tables::

    burl-manager migrate

Then create a new superuser::

    burl-manager createsuperuser

Now you should be ready to run ``burl``!  You can run a test/development server
by running ``burl-manager runserver`` to ensure that everything is working. In
production, you should deploy behind a WSGI server.

Configuration
=============

``burl`` adds two extra layers of configuration on top of the default Django
settings mechanism.

Configuration Notes
-------------------

Email
~~~~~

If you want working email (e.g. for password resets) the only supported option
at this time is to use sendgrid.  Set the environment variable
``BURL_SENDGRID_API_KEY`` to enable sendgrid support. Otherwise all email is
printed to the console and never sent.

Environment Variables
---------------------

Required Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Per the 12-factor app, secrets are read from environment variables. The following
environment variables must be set::

    BURL_SECRET_KEY="***********************************************"
    BURL_POSTGRES_PASSWORD="***********"

There are a variety of ways you can set these variables, using your system's
init system, or your organization's infrastructure secrets management tools.

Failing to set these variables will raise an ``ImproperlyConfigured`` exception.

Optional Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shown here with default values::

    BURL_API_PAGE_SIZE=100
    BURL_APP_LOG_LEVEL=INFO
    BURL_HASHID_ALPHABET=abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ0123456789
    BURL_LOG_LEVEL=WARNING
    BURL_MEDIA_ROOT=$HOME/var/burl/media
    BURL_POSTGRES_DB=burl
    BURL_POSTGRES_HOST=127.0.0.1
    BURL_POSTGRES_PORT=5432
    BURL_POSTGRES_USER=burl
    BURL_SENDGRID_API_KEY=''
    BURL_STATIC_ROOT=$HOME/share/burl/static
    BURL_TIMEZONE=America/Los_Angeles

Configuration File
------------------

``burl`` is also configurable via an external configuration file; it will try
each of the following paths in order, and will use the first file it finds:

#. ``/etc/burl/burlrc``
#. ``$HOME/.config/burl/burlrc``
#. ``$HOME/etc/burl/burlrc``

The ``burlrc`` file is loaded as a python module, after all other django settings
are loaded.  Settings configured in ``burlrc`` will override previously-defined
settings. ``burlrc`` can contain arbitrary python code, just like any Django settings
module; and just like Django settings modules, only variables in ALL_CAPS are
loaded.


Deployment
==========

Standard Python
---------------

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
you can change on the ``docker build`` command line.

This container does not include postgres or nginx. You will need postgres to run
burl, and you will want to put nginx in front of the container.


Development
===========

``burl`` uses `pipenv <https://docs.pipenv.org/>`_ for managing dependencies
and virtualenvs for development.
`Why Python devs should use Pipenv <https://opensource.com/article/18/2/why-python-devs-should-use-pipenv>`_
provides a nice explainer.

When using ``pipenv`` you can make use of a ``.env`` file in the source root,
and set the requisite environment variables (above) there.
