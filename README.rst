==========
Background
==========

This demo server relates to the publication **Hoffmann et al. "Data integration between clinical research and patient care: a framework for context-depending data sharing and in silico predictions"**, submitted for publication to PLOS Digital Health (2022).

Developer documentation, including initial installation instructions, is available in Sphinx format in the docs directory. For information on creating HTML output, see section `Building Documentation`_.

.. note::
    This repository also contains the computational models (``demo_model.zip``) that have to be implemented in the Model and Simulation Server "MAGPIE" and sample datasets (``demo_db.sqlite3``, ``demo_media.zip``) that can be used for testing the Clinic view and the Research view. Brief instructions on how to set up the test server can be found in section `Quickstart`_.
    For testing purposes, we provide a demo instance of the MOSAIC TTP (Trusted Third Party) server that contains the identifying patient data, the consents, and the pseudonyms used in the test environment.


==========
Quickstart
==========

To bootstrap the test server::

    virtualenv env
    source path/to/env/bin/activate
    cd path/to/predictDemo/repository
    pip install -r requirements.pip
    cp predictDemo/settings/local.py.example predictDemo/settings/local.py
    
Unzip ``demo_media.zip`` to ``media`` folder in ``path/to/predict/repository/`` directory.

Start the Server::
    
    python manage.py runserver

Happy Testing!

======================
Building Documentation
======================

Documentation is available in ``docs`` and can be built into a number of 
formats using `Sphinx <http://pypi.python.org/pypi/Sphinx>`_. To get started::

    cd docs
    make html

This creates the documentation in HTML format at ``docs/_build/html``.