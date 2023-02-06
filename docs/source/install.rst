====================
Initial installation
====================

Pre-Requisites
===============

* Install `python3 <https://www.python.org>`_.
* Install `virtual environment <https://virtualenv.pypa.io/en/latest/>`_ and `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_.
* Install a database management system that is `supported by Django <https://docs.djangoproject.com/en/4.1/ref/databases/>`_, create and configure a database.
* Install and configure the `MOSAIC Tools <https://www.ths-greifswald.de/projekte/mosaic-projekt/>`_.
* Install and configure the `MAGPIE Model and Simulation Server <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005898/>`_.
* Install `R <https://cloud.r-project.org>`_ and the R packages `christbald/magpie_api_r <https://doi.org/10.1371/journal.pcbi.1005898>`_, `RODBC <https://cran.r-project.org/web/packages/RODBC/index.html>`_, `ggplot <https://cran.r-project.org/web/packages/ggplot2/index.html>`_ and `devtools <https://cran.r-project.org/web/packages/devtools/index.html>`_ **that are required for the computational analytic in the Research view**::


To bootstrap the project
========================

* Create a clean base environment using virtualenv and virtualenvwrapper **outside** the project directory::

    mkvirtualenv -p /usr/bin/python3 <venv-name>

* Install required packages from file ``requirements.pip``::

    pip install -r requirements.pip

* Configure the environment by creating and editing the setting file ``local.py`` or ``production.py``::
    
    cp predictDemo/settings/local.py.example predictDemo/settings/local.py

* Applying database schema::

    python manage.py migrate [--settings=predictDemo.settings.local]

* Create a super user with admin privileges::

    python manage.py createsuperuser [--settings=predictDemo.settings.local]

* Synchronize role permissions with specific settings to admin interface::

    python manage.py sync_roles [--settings=predictDemo.settings.local]

* Run server::

    python manage.py runserver [--settings=predictDemo.settings.local]

To connect the MOSAIC TTP Server
================================

* Go to **Django Admin > Authentication and Authorization > Groups** and amend the fields ``TTP StudyId`` and ``TTP TargetIDType`` to the groups **dept_haematology** and **trial_cml**. Both values for each group have to be configured in the dispatcher module of the MOSAIC TTP server. 

This can be done:


#. ... by modifying the pre-configured XML entry located in the database ``ttp_dispatcher``, table ``configuration``, column ``configKey`` of the dataset ``dispatcher.config.1``. For each group, a new study with name ``<TTP StudyId>`` must be added and associated with the corresponding consent, represented as domain in the gICS module of the MOSAIC TTP server, and the organizational entity (identity), represented as domain in the EPIX module of the MOSAIC TTP server.


#. ... by adding an entry (alias) for each group to the database ``ttp_dispatcher``, table ``alias`` with values ``<TTP TargetIDType>`` as ``alias`` and ``"PSN"`` as ``aliasContext``. The alias ``<TTP TargetIDType>`` corresponds to the domain in the gPAS module of the MOSAIC TTP server. The domain in gPAS has to be named ``system.<TTP TargetIDType>``.
