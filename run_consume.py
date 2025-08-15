import time
import asyncio
from rabbit.consumer import get_rabbitmq_consumer


# await producer.publish("test_queue", "Привет из продюсера!")


async def process_message(message):
    time.sleep(10)
    print("Получено сообщение:", message.body.decode())
    await message.ack()


async def main():
    async with get_rabbitmq_consumer() as consumer:

        cons_channel = await consumer.create_channel()

        await consumer.consume(
            channel=cons_channel,
            routing_key="news",
            callback=process_message,
        )

        print("Консьюмер запущен и слушает очередь...")
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            print("Консьюмер остановлен")


if __name__ == "__main__":
    asyncio.run(main())
