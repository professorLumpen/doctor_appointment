from aio_pika import Message, DeliveryMode

from analytics.rabbit_base import RabbitBase
from analytics.retry_rabbit import RetryRabbitMixin


class RetryProducer(RabbitBase, RetryRabbitMixin):
    async def publish_message(
            self,
            message: str,
    ):
        _, queue = await self.declare_retry_queues()

        message = Message(
            body=message.encode("utf-8"),
            delivery_mode=DeliveryMode.PERSISTENT,
        )

        await self.channel.default_exchange.publish(
            message=message,
            routing_key=queue.name,
        )
