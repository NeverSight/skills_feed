---
name: edge-iot
description: Edge computing, IoT protocols, and embedded systems integration
domain: development-stacks
version: 1.0.0
tags: [edge, iot, mqtt, embedded, raspberry-pi, arduino, esp32]
triggers:
  keywords:
    primary: [iot, edge, embedded, mqtt, raspberry pi, arduino, esp32]
    secondary: [sensor, actuator, microcontroller, firmware, zigbee, bluetooth]
  context_boost: [device, hardware, physical, smart home]
  context_penalty: [web, frontend, cloud, saas]
  priority: medium
---

# Edge Computing & IoT

## Overview

Building applications for edge devices, IoT protocols, and embedded systems integration.

---

## MQTT Protocol

### Broker Setup (Mosquitto)

```yaml
# docker-compose.yml
services:
  mosquitto:
    image: eclipse-mosquitto:2
    ports:
      - "1883:1883"
      - "9001:9001"
    volumes:
      - ./mosquitto.conf:/mosquitto/config/mosquitto.conf
      - mosquitto_data:/mosquitto/data
      - mosquitto_log:/mosquitto/log

volumes:
  mosquitto_data:
  mosquitto_log:
```

```conf
# mosquitto.conf
listener 1883
listener 9001
protocol websockets

allow_anonymous false
password_file /mosquitto/config/passwd

persistence true
persistence_location /mosquitto/data/
log_dest file /mosquitto/log/mosquitto.log
```

### Node.js MQTT Client

```typescript
import mqtt from 'mqtt';

class MQTTClient {
  private client: mqtt.MqttClient;
  private subscriptions = new Map<string, Set<Function>>();

  constructor(brokerUrl: string, options?: mqtt.IClientOptions) {
    this.client = mqtt.connect(brokerUrl, {
      clientId: `node_${Math.random().toString(16).slice(2, 10)}`,
      clean: true,
      reconnectPeriod: 5000,
      ...options,
    });

    this.client.on('connect', () => {
      console.log('MQTT connected');
      // Resubscribe to all topics
      this.subscriptions.forEach((_, topic) => {
        this.client.subscribe(topic);
      });
    });

    this.client.on('message', (topic, payload) => {
      const handlers = this.getMatchingHandlers(topic);
      const message = this.parsePayload(payload);

      handlers.forEach(handler => handler(topic, message));
    });

    this.client.on('error', (error) => {
      console.error('MQTT error:', error);
    });
  }

  subscribe(topic: string, handler: (topic: string, message: any) => void) {
    if (!this.subscriptions.has(topic)) {
      this.subscriptions.set(topic, new Set());
      this.client.subscribe(topic);
    }

    this.subscriptions.get(topic)!.add(handler);

    return () => {
      this.subscriptions.get(topic)?.delete(handler);
      if (this.subscriptions.get(topic)?.size === 0) {
        this.subscriptions.delete(topic);
        this.client.unsubscribe(topic);
      }
    };
  }

  publish(topic: string, message: any, options?: mqtt.IClientPublishOptions) {
    const payload = typeof message === 'string'
      ? message
      : JSON.stringify(message);

    this.client.publish(topic, payload, {
      qos: 1,
      ...options,
    });
  }

  private getMatchingHandlers(topic: string): Set<Function> {
    const handlers = new Set<Function>();

    this.subscriptions.forEach((topicHandlers, pattern) => {
      if (this.topicMatches(pattern, topic)) {
        topicHandlers.forEach(h => handlers.add(h));
      }
    });

    return handlers;
  }

  private topicMatches(pattern: string, topic: string): boolean {
    const patternParts = pattern.split('/');
    const topicParts = topic.split('/');

    for (let i = 0; i < patternParts.length; i++) {
      if (patternParts[i] === '#') return true;
      if (patternParts[i] === '+') continue;
      if (patternParts[i] !== topicParts[i]) return false;
    }

    return patternParts.length === topicParts.length;
  }

  private parsePayload(payload: Buffer): any {
    const str = payload.toString();
    try {
      return JSON.parse(str);
    } catch {
      return str;
    }
  }

  disconnect() {
    this.client.end();
  }
}

// Usage
const mqtt = new MQTTClient('mqtt://localhost:1883', {
  username: 'user',
  password: 'pass',
});

// Subscribe to device telemetry
mqtt.subscribe('devices/+/telemetry', (topic, data) => {
  const deviceId = topic.split('/')[1];
  console.log(`Device ${deviceId}:`, data);
});

// Subscribe to all events from a device
mqtt.subscribe('devices/sensor-001/#', (topic, data) => {
  console.log(`${topic}:`, data);
});

// Publish command to device
mqtt.publish('devices/sensor-001/commands', {
  action: 'reboot',
  timestamp: Date.now(),
});
```

### Device Simulator

```typescript
class DeviceSimulator {
  private mqtt: MQTTClient;
  private deviceId: string;
  private interval: NodeJS.Timeout | null = null;

  constructor(deviceId: string, brokerUrl: string) {
    this.deviceId = deviceId;
    this.mqtt = new MQTTClient(brokerUrl);

    // Subscribe to commands
    this.mqtt.subscribe(`devices/${deviceId}/commands`, (_, command) => {
      this.handleCommand(command);
    });
  }

  start(intervalMs = 5000) {
    this.interval = setInterval(() => {
      this.sendTelemetry();
    }, intervalMs);
  }

  stop() {
    if (this.interval) {
      clearInterval(this.interval);
      this.interval = null;
    }
  }

  private sendTelemetry() {
    const telemetry = {
      temperature: 20 + Math.random() * 10,
      humidity: 40 + Math.random() * 20,
      pressure: 1013 + Math.random() * 10,
      battery: 85 + Math.random() * 15,
      timestamp: Date.now(),
    };

    this.mqtt.publish(`devices/${this.deviceId}/telemetry`, telemetry);
  }

  private handleCommand(command: any) {
    console.log(`Received command:`, command);

    switch (command.action) {
      case 'reboot':
        this.mqtt.publish(`devices/${this.deviceId}/status`, {
          status: 'rebooting',
          timestamp: Date.now(),
        });
        break;

      case 'update_config':
        // Update local config
        break;
    }
  }
}
```

---

## Edge Functions

### Cloudflare Workers for IoT

```typescript
// Edge function to process IoT data
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // Device telemetry ingestion
    if (url.pathname === '/ingest' && request.method === 'POST') {
      const data = await request.json();
      const deviceId = request.headers.get('X-Device-ID');

      // Validate device
      const device = await env.KV.get(`device:${deviceId}`);
      if (!device) {
        return new Response('Unauthorized', { status: 401 });
      }

      // Process at edge
      const processed = processData(data);

      // Store in Durable Object for aggregation
      const aggregator = env.AGGREGATOR.get(
        env.AGGREGATOR.idFromName(deviceId)
      );
      await aggregator.fetch(request.url, {
        method: 'POST',
        body: JSON.stringify(processed),
      });

      // Forward to origin if needed
      if (processed.alert) {
        await fetch('https://api.example.com/alerts', {
          method: 'POST',
          body: JSON.stringify({
            deviceId,
            alert: processed.alert,
          }),
        });
      }

      return new Response('OK');
    }

    return new Response('Not Found', { status: 404 });
  },
};

function processData(data: any) {
  // Edge processing logic
  const alert = data.temperature > 30 ? 'HIGH_TEMP' : null;

  return {
    ...data,
    processedAt: Date.now(),
    alert,
  };
}

// Durable Object for stateful aggregation
export class DeviceAggregator {
  private state: DurableObjectState;
  private readings: any[] = [];

  constructor(state: DurableObjectState) {
    this.state = state;
  }

  async fetch(request: Request): Promise<Response> {
    const data = await request.json();

    this.readings.push(data);

    // Keep last 100 readings
    if (this.readings.length > 100) {
      this.readings.shift();
    }

    // Compute aggregates
    const aggregates = {
      avgTemperature: this.average('temperature'),
      avgHumidity: this.average('humidity'),
      count: this.readings.length,
    };

    await this.state.storage.put('aggregates', aggregates);

    return new Response(JSON.stringify(aggregates));
  }

  private average(field: string): number {
    const values = this.readings
      .map(r => r[field])
      .filter(v => typeof v === 'number');

    return values.reduce((a, b) => a + b, 0) / values.length;
  }
}
```

---

## Embedded Systems (ESP32/Arduino)

### ESP32 with MicroPython

```python
# boot.py - WiFi connection
import network
import time

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(ssid, password)

        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1

    if wlan.isconnected():
        print('Connected:', wlan.ifconfig())
        return True
    else:
        print('Failed to connect')
        return False

connect_wifi('MyNetwork', 'password')
```

```python
# main.py - Sensor reading and MQTT
from machine import Pin, ADC
from umqtt.simple import MQTTClient
import json
import time
import dht

# Configuration
MQTT_BROKER = '192.168.1.100'
DEVICE_ID = 'esp32-001'
TOPIC_TELEMETRY = f'devices/{DEVICE_ID}/telemetry'
TOPIC_COMMANDS = f'devices/{DEVICE_ID}/commands'

# Hardware setup
led = Pin(2, Pin.OUT)
dht_sensor = dht.DHT22(Pin(4))
light_sensor = ADC(Pin(34))

# MQTT client
client = MQTTClient(DEVICE_ID, MQTT_BROKER)

def on_message(topic, msg):
    topic = topic.decode()
    data = json.loads(msg.decode())

    print(f'Command received: {data}')

    if data.get('action') == 'led_on':
        led.on()
    elif data.get('action') == 'led_off':
        led.off()
    elif data.get('action') == 'blink':
        for _ in range(5):
            led.on()
            time.sleep(0.2)
            led.off()
            time.sleep(0.2)

client.set_callback(on_message)
client.connect()
client.subscribe(TOPIC_COMMANDS)

def read_sensors():
    dht_sensor.measure()
    return {
        'temperature': dht_sensor.temperature(),
        'humidity': dht_sensor.humidity(),
        'light': light_sensor.read(),
        'timestamp': time.time()
    }

def main():
    last_publish = 0
    publish_interval = 5  # seconds

    while True:
        # Check for incoming messages
        client.check_msg()

        # Publish telemetry periodically
        current_time = time.time()
        if current_time - last_publish >= publish_interval:
            try:
                data = read_sensors()
                client.publish(TOPIC_TELEMETRY, json.dumps(data))
                print(f'Published: {data}')
                last_publish = current_time
            except Exception as e:
                print(f'Error: {e}')

        time.sleep(0.1)

if __name__ == '__main__':
    main()
```

### Arduino/C++ for ESP32

```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

// Configuration
const char* ssid = "MyNetwork";
const char* password = "password";
const char* mqtt_server = "192.168.1.100";
const char* device_id = "esp32-001";

// Hardware
#define DHT_PIN 4
#define DHT_TYPE DHT22
#define LED_PIN 2
#define LIGHT_PIN 34

DHT dht(DHT_PIN, DHT_TYPE);
WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastPublish = 0;
const long publishInterval = 5000;

void setup_wifi() {
    delay(10);
    Serial.println("Connecting to WiFi...");

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("\nWiFi connected");
    Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
    StaticJsonDocument<200> doc;
    deserializeJson(doc, payload, length);

    const char* action = doc["action"];

    if (strcmp(action, "led_on") == 0) {
        digitalWrite(LED_PIN, HIGH);
    } else if (strcmp(action, "led_off") == 0) {
        digitalWrite(LED_PIN, LOW);
    }
}

void reconnect() {
    while (!client.connected()) {
        Serial.println("Connecting to MQTT...");

        if (client.connect(device_id)) {
            Serial.println("Connected");

            char topic[50];
            sprintf(topic, "devices/%s/commands", device_id);
            client.subscribe(topic);
        } else {
            Serial.print("Failed, rc=");
            Serial.println(client.state());
            delay(5000);
        }
    }
}

void publishTelemetry() {
    StaticJsonDocument<200> doc;
    doc["temperature"] = dht.readTemperature();
    doc["humidity"] = dht.readHumidity();
    doc["light"] = analogRead(LIGHT_PIN);
    doc["timestamp"] = millis();

    char buffer[256];
    serializeJson(doc, buffer);

    char topic[50];
    sprintf(topic, "devices/%s/telemetry", device_id);
    client.publish(topic, buffer);

    Serial.println("Published telemetry");
}

void setup() {
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);
    dht.begin();

    setup_wifi();
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);
}

void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();

    unsigned long now = millis();
    if (now - lastPublish >= publishInterval) {
        lastPublish = now;
        publishTelemetry();
    }
}
```

---

## Device Management

### Device Registry

```typescript
interface Device {
  id: string;
  name: string;
  type: string;
  status: 'online' | 'offline' | 'error';
  lastSeen: Date;
  metadata: Record<string, any>;
  config: Record<string, any>;
}

class DeviceRegistry {
  constructor(
    private db: Database,
    private mqtt: MQTTClient
  ) {
    // Listen for device status
    this.mqtt.subscribe('devices/+/status', (topic, status) => {
      const deviceId = topic.split('/')[1];
      this.updateStatus(deviceId, status);
    });
  }

  async register(device: Omit<Device, 'status' | 'lastSeen'>) {
    const fullDevice: Device = {
      ...device,
      status: 'offline',
      lastSeen: new Date(),
    };

    await this.db.devices.create({ data: fullDevice });

    // Send initial config to device
    this.mqtt.publish(`devices/${device.id}/config`, device.config);

    return fullDevice;
  }

  async updateConfig(deviceId: string, config: Record<string, any>) {
    await this.db.devices.update({
      where: { id: deviceId },
      data: { config },
    });

    // Push config to device
    this.mqtt.publish(`devices/${deviceId}/config`, config, { retain: true });
  }

  async sendCommand(deviceId: string, command: any) {
    this.mqtt.publish(`devices/${deviceId}/commands`, command);

    // Log command
    await this.db.deviceCommands.create({
      data: {
        deviceId,
        command,
        timestamp: new Date(),
      },
    });
  }

  private async updateStatus(deviceId: string, status: any) {
    await this.db.devices.update({
      where: { id: deviceId },
      data: {
        status: status.status,
        lastSeen: new Date(),
      },
    });
  }
}
```

---

## Related Skills

- [[realtime-systems]] - Real-time communication
- [[cloud-platforms]] - IoT cloud services
- [[system-design]] - Edge architecture

