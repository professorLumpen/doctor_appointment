from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel

from analytics.exceptions import RabbitException
from app.config import settings


class RabbitBase:
    def __init__(
            self,
            connection_url: str = settings.rmq_url
    ):
        self.connection_url = connection_url
        self._connection: AbstractRobustConnection | None = None
        self._channel: AbstractRobustChannel | None = None

    async def __aenter__(self):
        self._connection = await connect_robust(self.connection_url)
        self._channel = await self._connection.channel()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
        self._connection = None
        self._channel = None

    @property
    def channel(self) -> AbstractRobustChannel:
        if self._channel is None:
            raise RabbitException("only context manager")
        return self._channel
