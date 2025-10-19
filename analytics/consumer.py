import asyncio
import random
from typing import Callable, Any

from aio_pika import Message
from aio_pika.abc import AbstractRobustChannel, DeliveryMode

from analytics.exceptions import RabbitException
from analytics.rabbit_base import RabbitBase
from analytics.retry_rabbit import RetryRabbitMixin
from app.config import settings


class RetryConsumer(RabbitBase, RetryRabbitMixin):
    async def consume_messages(
            self,
            callback_func: Callable,
            prefetch_count: int = 1
    ):
        await self.channel.set_qos(prefetch_count=prefetch_count)

        _, queue = await self.declare_retry_queues()

        async with queue.iterator() as queue_iterator:
            async for message in queue_iterator:
                try:
                    async with message.process():
                        await callback_func(message)
                except RabbitException as e:
                    print("Message not acknowledged:", e)


def extract_deaths_count(headers: dict[str, Any] | None) -> int:
    if headers and headers.get("x-death"):
        for props in headers.get("x-death"):
            if "count" in props:
                return int(props["count"])
    return 0


def is_error(error_probability: float = 0):
    return random.random() < error_probability


async def process_data(
        channel: AbstractRobustChannel,
        message: Message
):
    await asyncio.sleep(1)

    error = is_error(settings.ERROR_PROBABILITY)
    death_count = extract_deaths_count(message.headers)
    body_msg = message.body.decode()

    if not error:
        print("message acknowledged:", body_msg)
        return

    if death_count >= settings.DEATH_LIMIT:
        print(f"death limit reached. message '{body_msg}' sent to not solved queue")

        not_solved_message = Message(
            body=message.body,
            headers=message.headers,
            delivery_mode=DeliveryMode.PERSISTENT,
        )

        await channel.default_exchange.publish(
            message=not_solved_message,
            routing_key=settings.RMQ_NOT_SOLVED,
        )

        return

    print(f"message '{body_msg}' not acknowledged. death count: {death_count}. retrying")
    raise RabbitException("process data error")

