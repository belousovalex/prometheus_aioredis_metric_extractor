About
=====

Extract from Redis user metric values written with https://github.com/belousovalex/prometheus_aioredis_client


Install
=======

.. code-block:: bash

    $ pip install prometheus-aioredis-metric-extractor


Usage
=====

You can start up service as module and put file with list of metrics:


.. code-block:: bash

    $ python -m prometheus_aioredis_metric_extractor --source test_metric_list.txt  --redis-dsn redis://localhost:6380 --port 8987

where "source" is tab separated file with metric information:


.. code-block:: bash

    counter simple_counter  some doc string ololo
    histogram   simple_histogram    0,100,200   Simple Histogram Documentation
    gauge   simple_gauge    gauge doc
    summary simple_summary  summary doc

Columns

- metric type
- metric name
- buckets name (only for histogram)
- doc string


Or you can use Registry in code:

.. code-block:: python

    from prometheus_aioredis_metric_extractor import Extractor
    from mypackage import registry

    Extractor(
        registry=registry,
        redis_dsn="redis://localhost:6380"
    ).start_forever()

Also you can configure extractor via environment:

- EXTRACTOR_REDIS_DSN - redis connectiob dsn
- EXTRACTOR_POOL_SIZE - redis pool size
- EXTRACTOR_REDIS_TIMEOUT - redis request timeout
- EXTRACTOR_HOST - extractor host
- EXTRACTOR_PORT - extractor port
- EXTRACTOR_SOURCE - path file of metrics


