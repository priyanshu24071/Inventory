from fastapi import FastAPI, Request, HTTPException
import json
import time
import random
import logging
import requests

logging.basicConfig(level=logging.INFO)

app = FastAPI()


async def get_base_url(request: Request):
    return str(request.base_url)


PUBSUB_NAME = 'orderpubsub'
TOPIC = 'orders'
logging.info('Publishing to Pubsub Name: %s, Topic: %s' % (
    PUBSUB_NAME, TOPIC))


@app.get("/")
async def read_root(request: Request):
    base_url = await get_base_url(request)
    return {"message": "Welcome to the FastAPI Publisher", "base_url": base_url}


@app.get("/publish-orders")
async def publish_orders(request: Request):
    base_url = await get_base_url(request)
    for i in range(1, 10):
        order = {'orderId': i}

        # Publish an event/message using Dapr PubSub via HTTP Post
        result = requests.post(
            url='%s/v1.0/publish/%s/%s' % (base_url, PUBSUB_NAME, TOPIC),
            json=order
        )
        logging.info('Published data: ' + json.dumps(order))

        time.sleep(1)

    return {"message": "Orders published successfully"}


@app.get("/publish-crud")
async def publish_crud(request: Request):
    base_url = await get_base_url(request)
    # Simulate CRUD events
    crud_events = ["create", "read", "update", "delete"]

    for event in crud_events:
        event_data = {'event': event}

        # Publish an event/message using Dapr PubSub via HTTP Post
        result = requests.post(
            url='%s/v1.0/publish/%s/%s' % (base_url, PUBSUB_NAME, event),
            json=event_data
        )
        logging.info('Published CRUD event: ' + json.dumps(event_data))

        time.sleep(1)

    return {"message": "CRUD events published successfully"}
