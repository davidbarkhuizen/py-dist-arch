from typing import Any, Callable, Optional

from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from model.common import QueueEndpoint, Queue
from util.events import log_event, log_exception
from model.logevent import QueueListenerFailedToConnect, QueueListenerStartingConsumption, QueuePublisherConnected, QueuePublisherFailedToConnect
from pydantic import BaseModel
import pika
import json
import time, traceback

def connect_and_listen_blocking(ep: QueueEndpoint, on_message_callback: Callable):

    queue_name = ep.queue.value

    listen_connection = pika.BlockingConnection(pika.ConnectionParameters(host=ep.host, port=ep.port))
    listen_channel = listen_connection.channel()
    listen_channel.exchange_declare(exchange=ep.exchange)
    listen_channel.queue_declare(queue=queue_name, durable=True, exclusive=False, auto_delete=False)
    listen_channel.queue_bind(exchange=ep.exchange, queue=queue_name, routing_key=queue_name)

    def internal_on_message_callback(channel, method, properties, body):
        
        def ack():
            channel.basic_ack(delivery_tag = method.delivery_tag)

        as_dict: Optional[Any] = None
        try:
            as_dict = json.loads(body)
        except:
            log_exception('json deserialization in connect_and_listen_blocking.internal_on_message_callback')
            return

        on_message_callback(as_dict, ack)  

    listen_channel.basic_consume(queue=queue_name, on_message_callback=internal_on_message_callback, auto_ack=False)
    log_event(QueueListenerStartingConsumption(queue_name=queue_name))
    listen_channel.start_consuming()

def connect_blocking_q_listener(ep: QueueEndpoint, callback):
    while True:
        try:
            connect_and_listen_blocking(ep, callback)
        except pika.exceptions.AMQPConnectionError:
            log_event(
                QueueListenerFailedToConnect(
                    queue_host=ep.host,
                    queue_port=ep.port,
                    queue_name=ep.queue.value,
                    error='pika.exceptions.AMQPConnectionError'
                )
            )   
        
        time.sleep(ep.retry_wait_s)
        continue

def get_configured_queue_publisher(ep: QueueEndpoint):

    connection: Optional[BlockingConnection] = None
    channel: Optional[BlockingChannel] = None

    def _disconnect():

        if channel:
            try:
                channel.close()
            except:
                pass

        if connection:
            try:
                connection.close()
            except:
                pass

    def _connect():
        nonlocal connection, channel
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=ep.host, port=ep.port))
        channel = connection.channel()
        channel.queue_declare(queue=ep.queue.value, durable=True, exclusive=False, auto_delete=False)

    def _publish(model: BaseModel):
        channel.basic_publish(
            exchange=ep.exchange,
            routing_key=ep.queue.value,
            body=model.json(),
            properties=pika.BasicProperties(
                content_type='text/plain',
                delivery_mode=2 # durable, persist to disk
            )
        )

    def _send(model: BaseModel):
        try:
            _publish(model)
        except:
            _disconnect()
            _connect()
            _publish(model)

    _connect()
    
    return _send

def wait_for_configured_queue_publisher(ep: QueueEndpoint):
    while True:
        try:
            publisher = get_configured_queue_publisher(ep)
            log_event(QueuePublisherConnected(queue_name=ep.queue.value))
            return publisher
        except:
            log_event(
                QueuePublisherFailedToConnect(
                    queue_host=ep.host,
                    queue_port=ep.port,
                    queue_name=ep.queue.value, 
                    info=traceback.format_exc(),
                )
            )
            time.sleep(float(ep.retry_wait_s))