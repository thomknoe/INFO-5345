import time
import board
import neopixel
from paho.mqtt import client as mqtt_client

BROKER = "10.56.129.182"   # same broker IP
PORT = 1883
TOPIC = "cube/+/emotion"

pixel_pin = board.D13
num_pixels = 7
brightness = 0.3
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=brightness,
                           auto_write=False, pixel_order=neopixel.GRB)

colors = {
    1: (0, 0, 0),
    2: (0, 0, 0),
    3: (0, 0, 0),
}

def blend_colors(c1, c2, c3):
    r = int((c1[0] + c2[0] + c3[0]) / 3)
    g = int((c1[1] + c2[1] + c3[1]) / 3)
    b = int((c1[2] + c2[2] + c3[2]) / 3)
    return (r, g, b)

def on_message(client, userdata, msg):
    topic_parts = msg.topic.split("/")
    cube_id = int(topic_parts[1])
    try:
        r, g, b = [int(x) for x in msg.payload.decode().split(",")]
        colors[cube_id] = (r, g, b)
        print(f"Cube {cube_id} -> {r,g,b}")
        # Update ring: two LEDs per cube
        cube_led_map = {1: [0, 1], 2: [2, 3], 3: [4, 5]}
        for idx in cube_led_map[cube_id]:
            pixels[idx] = (r, g, b)
        # Center LED blends all three
        center = blend_colors(colors[1], colors[2], colors[3])
        pixels[6] = center
        pixels.show()
    except Exception as e:
        print("Error parsing message:", e)

client = mqtt_client.Client("central_aggregator")
client.on_message = on_message
client.connect(BROKER, PORT)
client.subscribe(TOPIC)
client.loop_start()

print("Aggregator listening for cube colors...")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping...")
    pixels.fill((0, 0, 0))
    pixels.show()
    client.loop_stop()
