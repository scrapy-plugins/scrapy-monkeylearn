# scrapy-monkeylearn [![Build Status](https://travis-ci.org/tryolabs/scrapy-monkeylearn.svg?branch=master)](https://travis-ci.org/tryolabs/scrapy-monkeylearn)

A [Scrapy][scrapy] pipeline to categorize items using [MonkeyLearn][ml].

# Settings

         Option Name            |                         Value                         |    Example Value
------------------------------- | ----------------------------------------------------- | -------------------
`MONKEYLEARN_ENABLED`           | Whether to enable monkeylearn extension. Default=True | `True`
`MONKEYLEARN_CLASSIFIER`        | The ID of the classifier.                             | `'cl_0123abcd'`
`MONKEYLEARN_AUTH_TOKEN`        | The auth token.                                       | `'TWFuIGlzIGRp...'`
`MONKEYLEARN_CLASSIFIER_FIELDS` | A list of Item text fields to use for classification. | `['title', 'desc']`
`MONKEYLEARN_CATEGORIES_FIELD`  | The field where the category will be stored.          | `'categories'`

An example value of the `MONKEYLEARN_CATEGORIES_FIELD` field after classification
is: `[{'label': 'English', 'probability': 0.321}]`.

# License

Copyright (c) 2015 [Tryolabs][tryo] SRL.

Released under the MIT license.

[scrapy]: http://scrapy.org/
[ml]: http://www.monkeylearn.com/
[tryo]: http://tryolabs.com/
