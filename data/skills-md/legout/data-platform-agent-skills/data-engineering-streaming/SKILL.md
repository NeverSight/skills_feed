---
name: data-engineering-streaming
description: "Real-time data pipelines with Apache Kafka, MQTT (IoT), and NATS JetStream. Covers producers, consumers, streaming patterns, and integration with data platforms."
dependsOn: ["@data-engineering-core"]
---

# Streaming Data Systems

Real-time data ingestion and stream processing with Apache Kafka, MQTT, and NATS JetStream. Covers producers, consumers, and stream processing patterns for data engineering pipelines.

## Quick Comparison

| Feature | Apache Kafka | MQTT | NATS JetStream |
|---------|--------------|------|----------------|
| **Use Case** | High-throughput event streaming | IoT, mobile, constrained devices | Cloud-native, microservices |
| **Throughput** | Millions/sec | Thousands/sec | Hundreds of thousands/sec |
| **Durability** | Disk-based log, replayable | Ephemeral (configurable) | Disk-based persistence |
| **Ordering** | Per-partition | N/A (topic-based) | Per-subject |
| **Python Client** | confluent-kafka | paho-mqtt | nats-py |
| **Best For** | Event sourcing, CDC, log aggregation | Sensor data, telemetry | Service-to-service messaging |

## When to Use Which?

- **Kafka**: High-volume event streams, log aggregation, CDC, data lake ingestion
- **MQTT**: IoT devices, mobile push, constrained networks
- **NATS JetStream**: Microservices, request-reply, cloud-native, simpler ops than Kafka

## Skill Dependencies

- `@data-engineering-core` - Process stream data with Polars/DuckDB
- `@data-engineering-orchestration` - Orchestrate stream processing jobs
- `@data-engineering-quality` - Validate streaming data
- `@data-engineering-storage-lakehouse` - Persist streams to Delta/Iceberg

---

## Detailed Guides

### Apache Kafka

Install: `pip install confluent-kafka`

#### Producer
```python
from confluent_kafka import Producer
import socket
import json

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered to {msg.topic()} [{msg.partition()}]")

conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': socket.gethostname(),
    'acks': 'all'  # Wait for all replicas
}

producer = Producer(conf)

# Send messages asynchronously
for i in range(100):
    data = {'id': i, 'event': 'user_activity', 'value': i * 10}
    producer.produce(
        topic='user_activity_events',
        key=str(i),
        value=json.dumps(data).encode('utf-8'),
        callback=delivery_report
    )
    producer.poll(0)  # Trigger callbacks

producer.flush()  # Wait for delivery

# With Schema Registry (Avro)
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

schema_registry_client = SchemaRegistryClient({'url': 'http://localhost:8081'})
avro_serializer = AvroSerializer(schema_registry_client, schema_str)

producer = SerializingProducer({
    'bootstrap.servers': 'localhost:9092',
    'key.serializer': StringSerializer('utf_8'),
    'value.serializer': avro_serializer,
})
```

#### Consumer
```python
from confluent_kafka import Consumer, KafkaError

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,  # Manual commit
    'max.poll.interval.ms': 300000
}

consumer = Consumer(conf)
consumer.subscribe(['user_activity_events'])

try:
    while True:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            raise KafkaException(msg.error())

        # Process message
        data = json.loads(msg.value().decode('utf-8'))
        print(f"Received: {data}")

        # Manual commit after processing
        consumer.commit(asynchronous=False)

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
```

#### Stream Processing (ksqlDB pattern)
For complex transformations, use ksqlDB or Kafka Streams. REST API example:
```python
import requests

ksql_query = {
    "ksql": """
        SELECT id,
               COUNT(*) AS event_count,
               SUM(value) AS total_value
        FROM user_activity_events
        WINDOW TUMBLING (SIZE 1 MINUTE)
        GROUP BY id
        EMIT CHANGES
    """
}

response = requests.post("http://localhost:8088/query", json=ksql_query)
for line in response.iter_lines():
    print(line)
```

### MQTT for IoT

Install: `pip install paho-mqtt`

#### Publisher
```python
import paho.mqtt.client as mqtt
import json
import time

broker = "broker.emqx.io"
topic = "iot/sensors/temperature"

client = mqtt.Client(client_id="publisher_1", protocol=mqtt.MQTTv5)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print(f"Connection failed: {rc}")

client.on_connect = on_connect
client.connect(broker)
client.loop_start()

for i in range(10):
    payload = {
        "sensor_id": "temp_sensor_1",
        "temperature": 20 + i * 0.5,
        "humidity": 45 + i,
        "timestamp": time.time()
    }
    client.publish(
        topic=topic,
        payload=json.dumps(payload),
        qos=1  # At-least-once delivery
    )
    time.sleep(5)

client.loop_stop()
client.disconnect()
```

#### Subscriber
```python
def on_connect(client, userdata, flags, rc):
    client.subscribe(topic, qos=1)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode("utf-8"))
    print(f"[{msg.topic}] {payload}")

client.on_connect = on_connect
client.on_message = on_message
client.connect(broker)
client.loop_forever()
```

### NATS JetStream

Install: `pip install nats-py`

#### Producer/Consumer
```python
import asyncio
import nats

async def main():
    nc = await nats.connect("nats://localhost:4222")
    js = nc.jetstream()

    # Create stream
    await js.add_stream(
        name="events",
        subjects=["events.*"],
        storage="file",
        max_msgs=10000,
        max_age=3600
    )

    # Publish
    await js.publish("events.page_loaded", b'{"page": "/home"}')

    # Push consumer
    sub = await js.subscribe("events.*", durable="worker-1")
    async for msg in sub:
        print(f"Received: {msg.data.decode()}")
        await msg.ack()

    await nc.close()

asyncio.run(main())
```

#### Work Queue Pattern
```python
async def worker(name: str):
    nc = await nats.connect("nats://localhost:4222")
    js = nc.jetstream()
    sub = await js.subscribe("jobs.*", durable="workers", queue_group="processing")

    async for msg in sub:
        job_data = msg.data.decode()
        print(f"Worker {name} processing: {job_data}")
        await msg.ack()
    await nc.close()
```

---

## Production Patterns

### Idempotent Processing
Stream processors may receive duplicates. Design idempotent consumers:
```python
processed_ids = load_checkpoint()  # From DB/Redis
if msg.id in processed_ids:
    ack()  # Skip duplicate
else:
    process(msg)
    save_checkpoint(msg.id)
    ack()
```

### Batch Processing
```python
# Accumulate messages before writing to reduce DB load
batch = []
while True:
    msg = consumer.poll(timeout=0.1)
    if msg:
        batch.append(msg.value())
    if len(batch) >= BATCH_SIZE or timeout_reached:
        write_to_db(batch)
        consumer.commit()  # Commit after batch write
        batch.clear()
```

### Error Handling (Dead Letter Queue)
```python
try:
    process(msg)
except Exception as e:
    if is_retryable(e):
        nack(requeue=True)  # Retry
    else:
        produce_to_dlq(msg, str(e))  # Send to dead letter queue
        ack()
```

### Schema Evolution
- Use Avro/Protobuf with Schema Registry for compatibility
- Evolve schemas additively (new fields optional, old fields preserved)
- Register schemas per topic

---

## References

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [confluent-kafka Python Client](https://github.com/confluentinc/confluent-kafka-python)
- [MQTT 5.0 Specification](https://mqtt.org/mqtt5/)
- [NATS JetStream Documentation](https://docs.nats.io/jetstream/)
- `@data-engineering-orchestration` - Orchestrate consumers/producers as flows
