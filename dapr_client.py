from dapr.clients import DaprClient

class DaprPubSubClient:
    def __init__(self):
        
        self.dapr_client = DaprClient()

    async def publish_message(self, topic: str, data: dict):
        try:
            await self.dapr_client.publish_event(pubsub_name='pubsub', topic=topic, data=data)
            print(f"Published message to topic '{topic}': {data}")
        except Exception as e:
            print(f"Failed to publish message to topic '{topic}': {e}")

    async def subscribe_to_topic(self, topic: str, callback):
        try:
            await self.dapr_client.subscribe(pubsub_name='pubsub', topic=topic, callback=callback)
            print(f"Subscribed to topic '{topic}'")
        except Exception as e:
            print(f"Failed to subscribe to topic '{topic}': {e}")


async def handle_message(message):
    print(f"Received message: {message}")

async def main():
    dapr_client = DaprPubSubClient()
    await dapr_client.subscribe_to_topic(topic='my-topic', callback=handle_message)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
