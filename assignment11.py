import json
import time
import random
import threading

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "TEMPERATURE"


# Util

start_id = 111

def create_data():
    global start_id

    data = {
        "id": start_id,
        "device": "Sensor-A1",
        "time": time.asctime(),
        "temperature": round(random.uniform(20.0, 30.0), 2),
        "humidity": random.randint(40, 80),
        "status": random.choice(["OK", "WARNING"]),
        "location": {
            "room": "Lab11",
            "floor": 2
        }
    }

    start_id += 1
    return data


def print_data(data: dict):
    print("----- DATA RECEIVED -----")
    print(f"ID: {data.get('id')}")
    print(f"Device: {data.get('device')}")
    print(f"Time: {data.get('time')}")
    print(f"Temperature: {data.get('temperature')} °C")
    print(f"Humidity: {data.get('humidity')} %")
    print(f"Status: {data.get('status')}")

    location = data.get("location", {})
    print(f"Room: {location.get('room')}")
    print(f"Floor: {location.get('floor')}")
    print("-------------------------\n")


# Suscribe

def handle_message(client, userdata, message):
    try:
        decoded = message.payload.decode("utf-8")
        data = json.loads(decoded)
        print_data(data)
    except Exception as e:
        print("Error processing message:", e)


def start_subscriber():
    client = mqtt.Client(client_id="Subscriber")

    client.on_message = handle_message
    client.connect(BROKER, PORT, 60)
    client.subscribe(TOPIC)

    print("Subscriber started... listening\n")

    client.loop_forever()


# Publish

def publish_loop():
    client = mqtt.Client(client_id="Publisher")
    client.connect(BROKER, PORT, 60)

    while True:
        data = create_data()
        payload = json.dumps(data)

        client.publish(TOPIC, payload)
        print(f"Published: {payload}")

        time.sleep(3)


# Main

if __name__ == "__main__":
    # Start subscriber thread
    sub_thread = threading.Thread(target=start_subscriber)
    sub_thread.daemon = True
    sub_thread.start()

    # Start publisher thread
    pub_thread = threading.Thread(target=publish_loop)
    pub_thread.daemon = True
    pub_thread.start()

    # Keep main thread alive
    while True:
        time.sleep(1)
