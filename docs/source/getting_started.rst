Getting Started
===============

.. _installation:

Installation
------------

To use eia_client, first install it using pip. It is recommended
to install eia_client in a virtual environment.

.. code-block:: console

   (.venv) $ pip install eia_client


Most users can stop here. Unless you are planning on contributing
there is no need to go further.


.. _dev_setup:

Setup development environment
-----------------------------

Setup a development environment.

- Python 3.7+

Check python version.
.. code-block:: console
    
    $ python --version


.. code-block:: console

    $ git clone git@github.com:tayeva/eia-client-python.git

.. code-block:: console

    $ cd eia_client

Create a virtual environment (assume it's called ".venv").

.. code-block:: console

    (.venv) $ pip install -r requirements.txt


This is only recommended if you are developing.


.. code-block:: console

    (.venv) $ export PYTHONPATH=$PYTHONPATH:$(pwd)/src


.. _build_source:

Build from source
-----------------

Build this code from source.

.. code-block:: console

    $ git clone git@github.com:tayeva/eia-client-python.git

.. code-block:: console

    $ cd eia_client


Create a virtual environment (assume it's called ".venv").

.. code-block:: console

    (.venv) $ pip install -r requirements.txt


.. code-block:: console

    (.venv) $ python -m build