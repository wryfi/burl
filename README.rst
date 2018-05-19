####
burl
####

``burl`` (brief url) is a URL shortener written in Django. It has a simple REST API,
created using Django Rest Framework, allowing it to integrate seamlessly as a
microservice in many architectures.

``burl`` uses `hashids <https://github.com/davidaurelio/hashids-python>`_
against an object's primary key to produce short URL hashes.  While the
salt used by hashids is user-configurable, it should be noted that it is
technically possible to reverse hashid hashes.  For this application, an
enumeration attack is probably not a major threat, but you can decide that
for yourself.

Requirements
============

code
----

``burl`` is written in python 3.6 and django 2.0.  It will probably run fine
on python 3.4 and 3.5, but no effort at backwards compatibility is
made. Python 2 is not supported.  ``burl`` should run anywhere python
will run, most easily on a unix-like system.


database
--------

``burl`` requires a relational database.  Technically, any of the databases
supported by django should work at this time, but development is focused on
postgres, and future releases may introdudce postgres-specific code and/or
features. Therefore, ``psycopg2`` is a required dependency.

You will need database development libraries on your system to build the postgres
``psycopg2`` module needed for postgresql.

Installation
============

``burl`` is made to be installed via the standard python installation methods.
You can install it as simply as running::

    pip install burl

It is recommended, however, that you install ``burl`` in a virtualenv. For
development, in particular, the easiest way to set everything up is to use
``pipenv`` (see below).

Once you have installed ``burl``, you will need to create a database for its
use. The default configuration expects a database called ``burl``, owned by
a user named ``burl``, with a password specified in
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

Environment Variables
---------------------

Per the 12-factor app, secrets are read from environment variables. The following
environment variables must be set::

    BURL_SECRET_KEY="***********************************************"
    BURL_HASHID_SALT="*******"
    BURL_POSTGRES_PASSWORD="***********"

There are a variety of ways you can set these variables, using your system's
init system, or your organization's infrastructure secrets management tools.

Failing to set these variables will raise an ``ImproperlyConfigured`` exception.

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

``burl`` is a straightforward django app, with nothing fancy.

You can deploy burl with any WSGI-compliant web server. Running
`gunicorn <http://gunicorn.org/>`_ as the backend WSGI server, with an nginx
reverse proxy in front of it, is a common and well-supported configuration.

`Deploying Django <https://docs.djangoproject.com/en/2.0/howto/deployment/>`_
has some generic information about deploying django applications that you may
find useful if you are new to this stack.


Development
===========

``burl`` uses `pipenv <https://docs.pipenv.org/>`_ for managing dependencies
and virtualenvs for development.
`Why Python devs should use Pipenv <https://opensource.com/article/18/2/why-python-devs-should-use-pipenv>`_
provides a nice explainer.

When using ``pipenv`` you can make use of a ``.env`` file in the source root,
and set the requisite environment variables (above) there.
