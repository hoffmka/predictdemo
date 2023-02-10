========
REST-API
========

For demonstration purposes of how a potential integration with a CIS/EHR might look like, a REST API as a prototype is implemented to query all model predictions for a patient within a treatment context using the local CIS/EHR identifier. As result, the CIS/EHR receives a list of model predictions with metadata, including a link to a view of model results that can be accessed through or embedded in the system.

The API can be tested from command-line, using tools like ``curl``::

    curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"group":"dept_haematology","domain":"mdat","localName":"pat_id","localIdentifier":"111"}' https://predict.imb.medizin.tu-dresden.de/rest/request/predictions/rest/request/predictions/

or directly through the browser, by going to the URL  |location_link|

.. |location_link| raw:: html

   <a href="https://predict.imb.medizin.tu-dresden.de/rest/request/predictions" target="_blank">https://predict.imb.medizin.tu-dresden.de/rest/request/predictions/</a>

.. figure:: /img/request_predictions.png

Add the following content to the body of the POST request::

    {
        "group":"dept_haematology",
        "domain":"mdat",
        "localName":"pat_id",
        "localIdentifier":"111"
    }

``domain``, ``localName`` and ``localIdentifier`` are configured in the EPIX module of the MOSAIC TTP server, where ``localIdentifier`` is the CIS/EHR identifier for the patient within the ``domain``.

For testing purposes, the following local identifiers are defined for the patients implemented in the test instance of the MOSAIC TTP server::

    111 --> Max Mustermann
    222 --> Erika Mustermann
    333 --> Kari Nordmann
    444 --> Lieschen Müller
    555 --> Otto Normalo

The response of the POST request is a list of all finished model predictions of the requested patient within the specified treatment context. For each prediction, meta data and an url to a view with model results is available. The view (e.g., `<https://predict.imb.medizin.tu-dresden.de/predictions/detail/80/>`_) can be provided as a link in the CIS/EHR, for example.

.. figure:: /img/request_predictions2.png