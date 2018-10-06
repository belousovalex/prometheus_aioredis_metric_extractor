import os
from functools import partial

from aiohttp import web
from aioredis import create_redis_pool

from prometheus_aioredis_client import (
    Registry, TaskManager
)
from prometheus_aioredis_client.metrics import (
    Metric, Counter, Gauge, Summary, Histogram
)


class Extractor(object):

    def __init__(
            self,
            redis_dsn: str,
            pool_size: int=100,
            redis_timeout: int=10,
            host: str='0.0.0.0',
            port: int=9000,
            registry: Registry=None,
            source: str or None=None
        ):
        self.redis_dsn = redis_dsn
        self.host = host
        self.port = port
        self.pool_size = pool_size
        self.redis_timeout = redis_timeout
        if source is None and registry is None:
            raise Exception(
                "Registry' and list of metrics did not set."
            )
        self.source = source
        self._registry = registry

        self.metrics = self.runner = \
            self.redis = None

        self.app = web.Application()
        self.app.router.add_get('/metrics', self.metrics_view)
        self.app.on_startup.append(self.on_start)
        self.app.on_cleanup.append(self.on_stop)

    async def on_start(self, app):
        self.redis = await create_redis_pool(
            self.redis_dsn,
            maxsize=self.pool_size,
            timeout=self.redis_timeout
        )
        self.registry.set_redis(self.redis)

    async def on_stop(self, app):
        self.redis.close()
        await self.redis.wait_closed()

    async def metrics_view(self, request):
        return web.Response(
            body=(await self.registry.output()),
            content_type='text'
        )

    def start_forever(self):
        web.run_app(self.app, host=self.host, port=self.port)

    async def start(self):
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, self.host, self.port)
        await site.start()

    async def stop(self):
        await self.runner.cleanup()

    @property
    def registry(self):
        if not self._registry:
            self._registry = Registry(
                task_manager=TaskManager()
            )
            self.init_metrics()
        return self._registry

    def init_metrics(self):
        if not self.metrics:
            self.metrics = make_metrics_from_source(
                self.source, self._registry
            )

def make_metrics_from_source(source_file, registry: Registry) -> list:
    if not os.path.exists(source_file):
        raise Exception("Not found source file {}".format(
            source_file
        ))
    result = []
    with open(source_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            type, other = line.split("\t", 1)
            if type not in METRIC_MAPPING:
                raise TypeError("Type {} incorrect".format(
                    type
                ))
            result.append(
                METRIC_MAPPING[type](
                    other, registry
                )
            )
    return result


def make_metric(_class, other, registry: Registry) -> Metric:
    name, doc = other.split("\t", 1)
    return _class(
        name=name,
        documentation=doc,
        registry=registry
    )

def make_histogram(other, registry: Registry) -> Histogram:
    name, buckets, doc = other.split("\t", 2)
    buckets = [
        (int(b) if b.isdigit() else float(b))
        for b in buckets.split(",")
    ]
    return Histogram(
        name=name,
        documentation=doc,
        buckets=buckets,
        registry=registry
    )

METRIC_MAPPING = {
    'counter': partial(make_metric, Counter),
    'gauge': partial(make_metric, Gauge),
    'summary': partial(make_metric, Summary),
    'histogram': make_histogram,
}
