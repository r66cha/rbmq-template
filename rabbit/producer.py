"""RabbitMQ producer module."""

# -- Imports

from aio_pika import (
    connect_robust,
    Message,
    ExchangeType,
)
from contextlib import asynccontextmanager
from .config import RABBITMQ_URL

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aio_pika import RobustConnection, RobustChannel, ExchangeType


# -- Exports

__all__ = ["get_rabbitmq_producer"]

# --


class RabbitMQProducer:
    def __init__(self):
        self.connection: "RobustConnection" | None = None

    # --

    async def connect(self, url: str = RABBITMQ_URL):
        self.connection = await connect_robust(url)

    async def close(self):
        if self.connection:
            await self.connection.close()

    # --

    async def publish(
        self,
        channel: "RobustChannel",
        exchange_type: ExchangeType | str = ExchangeType.DIRECT,
        exchange_name: str = "direct_name",
        routing_key: str = "news",
        message: str = "Hello",
    ):

        exchange = await channel.declare_exchange(
            type=exchange_type,
            name=exchange_name,
            durable=True,
        )

        await exchange.publish(
            Message(body=message.encode()),
            routing_key=routing_key,
        )

    # --

    async def create_channel(self) -> "RobustChannel":
        if self.connection is None:
            raise RuntimeError("Connection is not established")
        return await self.connection.channel()


# --


@asynccontextmanager
async def get_rabbitmq_producer(url: str = RABBITMQ_URL):
    producer = RabbitMQProducer()
    await producer.connect(url)
    try:
        yield producer
    finally:
        await producer.close()


# --
