pyirl-todomvc README
==================

Overview
--------
This is an example SQLAlchemy / Cornice Application used as a demo
during a talk for Python Ireland.

The Javascript UI is one of the TODO MVC examples: https://github.com/tastejs/todomvc/tree/gh-pages/examples/emberjs

Setup the Postgresql DB
-----------------------

- Install via your package manager of choice

- Run the following steps to create a user, database and grant priveleges to that user
    dave@debian:~/PycharmProjects/pyirltodomvc$ su root
    Password:
    root@debian:/home/dave/PycharmProjects/pyirltodomvc# su - postgres
    postgres@debian:~$ createuser pyirltodomvc
    postgres@debian:~$ createdb pyirltodomvc
    postgres@debian:~$ psql
    psql (9.4.0)
    Type "help" for help.

    postgres=# GRANT ALL ON DATABASE pyirltodomvc TO pyIRLTODOMVC;
    GRANT
    postgres=# ALTER USER pyirltodomvc WITH PASSWORD 'pyirltodomvc';
    ALTER ROLE



Getting Started
---------------
- cd <directory containing this file>

- $VENV/bin/python setup.py develop

- $VENV/bin/initialize_pyirl-todomvc_db development.ini

- $VENV/bin/pserve development.ini
