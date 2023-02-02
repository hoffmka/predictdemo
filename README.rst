==================
Installation
==================

Pre-Requisites
===============

* Install `python3 <https://www.python.org>`_.
* Install `virtual environment <https://virtualenv.pypa.io/en/latest/>`_ and `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_.
* Optionally: Install `PostgreSQL <https://www.postgresql.org/download/>`_ or another database management system that is `supported by Django <https://docs.djangoproject.com/en/4.1/ref/databases/>`_.
* Create a database. In case of using Postgres SQL::
    
    sudo -u postgres psql
    CREATE DATABASE <db-name>;
    CREATE USER <db-user> WITH PASSWORD <db-password>;
    ALTER ROLE <db-user> SET client_encoding TO 'utf8';
    ALTER ROLE <db-user> SET default_transaction_isolation TO 'read committed';
    ALTER ROLE <db-user> SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE <db-name> TO <db-user>; 

* Install `R <https://cloud.r-project.org>`_::

    sudo add-apt-repository "deb http://cran.rstudio.com/bin/linux/ubuntu trusty/"
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9
    sudo add-apt-repository ppa:marutter/rdev
    sudo apt-get update
    sudo apt-get install -y r-base

* Install needed R packages::

    sudo apt install build-essential libcurl4-gnutls-dev libxml2-dev libssl-dev
    sudo -i R
    install.packages("devtools")
    require("devtools")
    install_github("christbald/magpie_api_r")
    install.packages("RODBC") # not more needed
    install.packages("ggplot2") # not more needed

* Install the `MOSAIC Tools <https://www.ths-greifswald.de/projekte/mosaic-projekt/>`_.
* Install the `MAGPIE Model and Simulation Server <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005898/>`_.
* Install Redis for Plotly Dash visualisations, see `Django-Plotly-Dash <https://django-plotly-dash.readthedocs.io/en/latest/installation.html#extra-steps-for-live-state>`_::

    docker pull redis:4
    docker run -p 6379:6379 -d redis

To bootstrap the Django project
===============================

* Create a clean base environment using virtualenv **outside** the project directory::

    mkvirtualenv -p /usr/bin/python3 <venv-name>

* Install required packages from file ``requirements.pip``::

    pip install -r requirements.pip

* Configure the environment by creating and editing the setting file ``local.py`` or ``production.py``::
    
    cp predicDemo/settings/local.py.example predicDemo/settings/local.py

* Applying database schema::

    python manage.py migrate [--settings=predictDemo.settings.local]

* Create a super user with admin privileges::

    python mange.py createsuperuser [--settings=predictDemo.settings.local]

* Synchronize role permissions with specific settings to admin interface::

    python manage.py sync_roles [--settings=predictDemo.settings.local]

* Run server::

    python manage.py runserver [--settings=predictDemo.settings.local]

Building Documentation
======================

Documentation is available in ``docs`` and can be built into a number of 
formats using `Sphinx <http://pypi.python.org/pypi/Sphinx>`_. To get started::

    cd docs
    make html

This creates the documentation in HTML format at ``docs/_build/html``.