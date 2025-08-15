import time
import asyncio
from rabbit.producer import get_rabbitmq_producer


async def main():
    async with get_rabbitmq_producer() as producer:

        prod_channel = await producer.create_channel()

        for i in range(10):
            msg = f"Hello {i}"
            time.sleep(1)
            print(f"Вывожу сообщение: {msg}")
            await producer.publish(
                channel=prod_channel,
                message=msg,
            )


if __name__ == "__main__":
    asyncio.run(main())
