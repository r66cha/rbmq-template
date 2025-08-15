"""RabbitMQ consumer module."""

# -- Imports

from aio_pika import connect_robust, ExchangeType
from typing import Callable
from contextlib import asynccontextmanager
from .config import RABBITMQ_URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aio_pika import RobustConnection, RobustChannel, ExchangeType


# -- Exports

__all__ = ["get_rabbitmq_consumer"]

# --


class RabbitMQConsumer:
    def __init__(self):
        self.connection: "RobustConnection" | None = None

    # --

    async def connect(self, url: str = RABBITMQ_URL):
        self.connection = await connect_robust(url)

    async def close(self):
        if self.connection:
            await self.connection.close()

    # --

    async def consume(
        self,
        channel: "RobustChannel",
        callback: Callable,
        exchange_type: ExchangeType | str = ExchangeType.DIRECT,
        exchange_name: str = "direct_name",
        routing_key: str = "news",
    ):
        queue = await channel.declare_queue(routing_key, durable=True)

        if exchange_name:
            exchange = await channel.declare_exchange(
                type=exchange_type,
                name=exchange_name,
                durable=True,
            )

            await queue.bind(exchange, routing_key)

        await queue.consume(callback)

    # --

    async def create_channel(self) -> "RobustChannel":
        if self.connection is None:
            raise RuntimeError("Connection is not established")
        return await self.connection.channel()


# --


@asynccontextmanager
async def get_rabbitmq_consumer(url: str = RABBITMQ_URL):
    consumer = RabbitMQConsumer()
    await consumer.connect(url)
    try:
        yield consumer
    finally:
        await consumer.close()


# --
