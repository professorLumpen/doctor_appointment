from typing import Any

from aio_pika.abc import AbstractRobustChannel, ExchangeType

from app.config import settings


class RetryRabbitMixin:
    channel: AbstractRobustChannel

    async def declare_exchange_and_queue(
            self,
            queue_name: str,
            exchange_name: str = "",
            exchange_type: ExchangeType = ExchangeType.DIRECT,
            durable: bool = True,
            arguments: dict[str, Any] | None = None,
    ):
        exchange = await self.channel.declare_exchange(
                name=exchange_name,
                type=exchange_type,
                durable=durable
            )

        queue = await self.channel.declare_queue(
            name=queue_name,
            durable=durable,
            arguments=arguments,
        )

        await queue.bind(exchange_name)

        return exchange, queue

    async def declare_not_solved_queue(
            self,
            queue_name: str = settings.RMQ_NOT_SOLVED,
            durable: bool = True,
    ):
        await self.channel.declare_queue(
            name=queue_name,
            durable=durable,
        )

    async def declare_retry_queues(self):
        await self.declare_not_solved_queue()

        main_exchange, main_queue = await self.declare_exchange_and_queue(
            queue_name=settings.RMQ_FOR_RETRIES,
            exchange_name=settings.RMX_FOR_RETRIES,
            arguments={
                "x-dead-letter-exchange": settings.DLX_FOR_RETRIES,
            }
        )

        await self.declare_exchange_and_queue(
            queue_name=settings.DLQ_FOR_RETRIES,
            exchange_name=settings.DLX_FOR_RETRIES,
            exchange_type=ExchangeType.FANOUT,
            arguments={
                "x-message-ttl": settings.TTL_FOR_RETRIES,
                "x-dead-letter-exchange": settings.RMX_FOR_RETRIES,
                "x-dead-letter-queue": settings.RMQ_FOR_RETRIES,
            }
        )

        return main_exchange, main_queue