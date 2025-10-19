from aio_pika import Message, DeliveryMode

from analytics.rabbit_base import RabbitBase
from analytics.retry_rabbit import RetryRabbitMixin
from app.config import settings


class RetryProducer(RabbitBase, RetryRabbitMixin):
    async def publish_message(
            self,
            message: bytes,
            queue_name: str = settings.RMQ_FOR_RETRIES,
    ):
        await self.declare_retry_queues()

        message = Message(
            body=message,
            delivery_mode=DeliveryMode.PERSISTENT,
        )

        await self.channel.default_exchange.publish(
            message=message,
            routing_key=queue_name,
        )
