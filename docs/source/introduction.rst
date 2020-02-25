==================
Introduction
==================

Background
==========

PrediCt Demonstrator is a software framework mainly designed to be used for clinicians to execute and visualize mathematical model predictions for treatment decision making at an individual patient level. This framework can be seen as a further development of the `HaematoOPT Demonstrator <https://hopt.imb.medizin.tu-dresden.de/>`_. It extends this framework with the integration of a pseudonymization service and access management. Furthermore, it can be used independendly of a clinical information system, because it is intended to be used within a data integration center (DIZ).

.. _Fictitous_data_flow_at_UKD:

Fictitous data flow at University Hospital Dresden
==================================================

The following figure presents fictitous data flows between patients (Consent Management), Clinical Information Systems (CIS), the Data Integration Center (DIC), the independant Trusted Third Party (TTH) and Researcher requests in consideration of data protection.

.. figure:: _static/figures/Workflow_UKD-3.pdf
   :alt: Fictitous Data flow at University Hospital Dresden


Possible Integration into clinical routine at University Hospital Dresden
=========================================================================

Using the example of the data integration center of the University Hospitel Dresden (see Fictitous_data_flow_at_UKD_), which is currently being established, the following figure describes a possible integration.

.. figure:: _static/figures/Workflow_PREDICT.svg
   :alt: Workflow of PrediCt Demonstrator

   Possible Integration of the PrediCt Application into the DIZ

