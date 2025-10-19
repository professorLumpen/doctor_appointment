import asyncio

from analytics.consumer import RetryConsumer, process_data


async def start_consuming():
    async with RetryConsumer() as consumer:
        await consumer.consume_messages(callback_func=process_data)


if __name__ == "__main__":
    asyncio.run(start_consuming())
