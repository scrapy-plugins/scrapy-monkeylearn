# scrapy-monkeylearn

A [Scrapy][scrapy] pipeline to categorize items using [MonkeyLearn][ml].

# Settings

         Option Name            |                         Value                         |    Example Value
------------------------------- | ----------------------------------------------------- | -------------------
`MONKEYLEARN_CLASSIFIER`        | The ID of the classifier.                             | `'0123abcd'`
`MONKEYLEARN_AUTH_TOKEN`        | The auth token.                                       | `'TWFuIGlzIGRp...'`
`MONKEYLEARN_CLASSIFIER_FIELDS` | A list of Item text fields to use for classification. | `['title', 'desc']`
`MONKEYLEARN_CATEGORY_FIELD`    | The field where the category will be stored.          | `'category'`

# License

Copyright (c) 2015 [Tryolabs][tryo] SRL.

Released under the MIT license.

[scrapy]: http://scrapy.org/
[ml]: http://www.monkeylearn.com/
[tryo]: http://tryolabs.com/
