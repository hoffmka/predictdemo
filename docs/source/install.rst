==================
Installation
==================

Pre-Requisites
===============

* Installing `python3 <https://www.python.org>`_.
* Installing `virtual environment <https://virtualenv.pypa.io/en/latest/>`_ and `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_
* Setting up Python3 as default Python Version and the virtual environment wrapper::

    # Editing the shell startup file
    sudo nano ~/.bash_profile
    # Content
    alias python='python3'
    export WORKON_HOME=/path/to/venvs
    source /usr/local/bin/virtualenvwrapper.sh
    # Save and Reload startup file
    source ~/.bash_profile

* Installing `PostgreSQL <https://www.postgresql.org/download/>`_.
* Installing `MS SQL Driver <https://docs.microsoft.com/de-de/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15>`_ for connecting to the Data Warehouse System based on MS SQL Server::
    
    # on Ubuntu 18.04 LTS
    # install dependencies
    sudo apt-get install libc6 libstdc++6 libkrb5-3 libcurl3 openssl debconf unixodbc unixodbc-dev
    # install Driver
    sudo dpkg -i msodbcsql17_17.4.2.1-1_amd64.deb

* Installing `R <https://cloud.r-project.org>`_::

    sudo add-apt-repository "deb http://cran.rstudio.com/bin/linux/ubuntu trusty/"
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9
    sudo add-apt-repository ppa:marutter/rdev
    sudo apt-get update
    sudo apt-get install -y r-base

* Installing shiny package::

    sudo R -e "install.packages('shiny', repos='https://cran.rstudio.com/')"
    # Run shiny application on port 8100
    sudo R -e "shiny::runApp(appDir='shinyapp', port=8100)"


Creating the Virtual Environment
================================

First, create a clean base environment using virtualenv **outside** the project directory::

    mkvirtualenv <venv-name>


Installing the Project
======================

Install the requirements and the project source::

    cd path/to/your/predicDemo/repository
    pip install -r requirements.pip


Configuring a Local Environment
===============================

First, create postgreSQL database::

    sudo -u postgres psql
    CREATE DATABASE <db-name>;
    CREATE USER <db-user> WITH PASSWORD <db-password>;

change settings::

    ALTER ROLE <db-user> SET client_encoding TO 'utf8';
    ALTER ROLE <db-user> SET default_transaction_isolation TO 'read committed';
    ALTER ROLE <db-user> SET timezone TO 'UTC';

and give database access rights to db-user:

    GRANT ALL PRIVILEGES ON DATABASE <db-name> TO <db-user>;

Second, copy example configuration file, edit and migrate database::

    cp predicDemo/settings/local.py.example predicDemo/settings/local.py
    manage.py migrate


Configuring the Role permissions
================================

synchronize role permissions with specific settings to admin interface::

    python manage.py sync_roles --settings=predicDemo.settings.local

Creating a superuser
====================

create a super user with admin privileges::

    python mange.py createsuperuser

Building Documentation
======================

Documentation is available in ``docs`` and can be built into a number of 
formats using `Sphinx <http://pypi.python.org/pypi/Sphinx>`_. To get started::

    cd docs
    make html

This creates the documentation in HTML format at ``docs/_build/html``.
