import os
from argparse import ArgumentParser

from prometheus_aioredis_client import REGISTRY
from .extractor import Extractor

def get_settings():
    parser = ArgumentParser()
    parser.add_argument(
        "--env-prefix", default="EXPORTER"
    )
    parser.add_argument(
        "--redis-dsn", default="redis://localhost:6379"
    )
    parser.add_argument(
        "--host", default="0.0.0.0"
    )
    parser.add_argument(
        "--port", default=9000,
        type=int
    )
    parser.add_argument(
        "--pool-size", default=100,
        type=int
    )
    parser.add_argument(
        "--redis-timeout", default=10,
        type=int
    )
    parser.add_argument("--source", required=False)
    args = parser.parse_args()

    return dict(
        pool_size=int(
            os.environ.get("{}_POOL_SIZE".format(
                args.env_prefix
            ), args.pool_size)
        ),
        redis_timeout=int(
            os.environ.get("{}_REDIS_TIMEOUT".format(
                args.env_prefix
            ), args.redis_timeout)
        ),
        host=(
            os.environ.get("{}_HOST".format(
                args.env_prefix
            ), args.host)
        ),
        port=int(
            os.environ.get("{}_PORT".format(
                args.env_prefix
            ), args.port)
        ),
        redis_dsn=os.environ.get("{}_REDIS_DSN".format(
            args.env_prefix
        ), args.redis_dsn),
        source=os.environ.get("{}_SOURCE".format(
            args.env_prefix
        ), args.source),
        registry=(
            None if args.source else
            REGISTRY
        ),
    )

kwargs = get_settings()
Extractor(**kwargs).start_forever()
