=====================
Software Architecture
=====================

The Application Server is written with the Python Web Framework `Django <https://www.djangoproject.com/>`_ and serveral Third Party Apps. It includes a `PostgresSQL <https://www.postgresql.org/>`_ database mainly for User Administration and Access Control. Furthermore, it embeds `Shiny <https://shiny.rstudio.com/>`_ Applications for data visualization and, with the extension of `MAGPIE <https://magpie.imb.medizin.tu-dresden.de/>`_ as simulation server, for presenting model predictions.

The access to the required medical data (MDAT) is done in 3 steps.

* 1. Request of the (model-dependend) pseudonym by MOSAIC as Trusted Third Party Tool via REST API.
* 2. Passing the pseudonym as parameter to Shiny App.
* 3. Request MDATS by Shiny App for visualization and passing MDATS from Shiny to MAGPIE for execution of model prediction.

The application is running on an `Apache <https://httpd.apache.org/>`_ Webserver. Next to it the `Nginx <https://www.nginx.com/>`_ Webserver is established as a reverse proxy in order to control the access to the Shiny Applications.
