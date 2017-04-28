scrapy-monkeylearn
==================

A `Scrapy`_ pipeline to categorize items using `MonkeyLearn`_.

Settings
--------

MONKEYLEARN_BATCH_SIZE
~~~~~~~~~~~~~~~~~~~~~~

The size of the item batches sent to MonkeyLearn.

Default: ``200``

Example:

.. code-block:: python

   MONKEYLEARN_BATCH_SIZE = 200

MONKEYLEARN_MODULE
~~~~~~~~~~~~~~~~~~

The ID of the monkeylearn module.

Example:

.. code-block:: python

    MONKEYLEARN_MODULE = 'cl_oFKL5wft'

MONKEYLEARN_USE_SANDBOX
~~~~~~~~~~~~~~~~~~~~~~~

In case of using a classifier, if the sandbox version should be used.

Default: ``False``

Example:

.. code-block:: python

    MONKEYLEARN_USE_SANDBOX = True

MONKEYLEARN_TOKEN
~~~~~~~~~~~~~~~~~

The auth token.

Example:

.. code-block:: python

    MONKEYLEARN_TOKEN = 'TWFuIGlzIGRp...'

MONKEYLEARN_FIELD_TO_PROCESS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A field or list of Item text fields to use for classification.
Also comma-separated string with field names is supported.

Example:

.. code-block:: python

    MONKEYLEARN_FIELD_TO_PROCESS = 'title'

.. code-block:: python

    MONKEYLEARN_FIELD_TO_PROCESS = ['title', 'description']

.. code-block:: python

    MONKEYLEARN_FIELD_TO_PROCESS = 'title,description'

MONKEYLEARN_FIELD_OUTPUT
~~~~~~~~~~~~~~~~~~~~~~~~

The field where the MonkeyLearn output will be stored.

Example:

.. code-block:: python

    MONKEYLEARN_FIELD_OUTPUT = 'categories'


An example value of the `MONKEYLEARN_FIELD_OUTPUT` field after classification is:

.. code-block:: python

    [{'label': 'English', 'probability': 0.321}]

Usage
-----

In your *settings.py* file, add the previously described settings and add ``MonkeyLearnPipeline`` to your pipelines, e.g.:

.. code-block:: python

    ITEM_PIPELINES = {
        'scrapy_monkeylearn.pipelines.MonkeyLearnPipeline': 100,
    }

License
-------

Copyright (c) 2015 `MonkeyLearn`_.

Released under the MIT license.

.. _Scrapy: http://scrapy.org/
.. _MonkeyLearn: http://www.monkeylearn.com/
