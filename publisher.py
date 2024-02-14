from dapr.clients import DaprClient
import json
import time
import logging

logging.basicConfig(level=logging.INFO)

with DaprClient() as client:
    for i in range(1, 10):
        item = {'itemId': i}
        # Publish an event/message using Dapr PubSub
        result = client.publish_event(
            pubsub_name='itempubsub',
            topic_name='items',
            data=json.dumps(item),
            data_content_type='application/json',
        )
        logging.info('Published data: ' + json.dumps(item))
        time.sleep(1)
