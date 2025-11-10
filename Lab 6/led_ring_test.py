import board
import neopixel
import time

# --- Configuration ---
pixel_pin = board.D18   # GPIO 18 pin (Pin 12 on header)
num_pixels = 7          # number of LEDs on your ring
brightness = 0.3        # between 0.0 and 1.0

# --- Initialize NeoPixel ring ---
pixels = neopixel.NeoPixel(
    pixel_pin,
    num_pixels,
    brightness=brightness,
    auto_write=False,
    pixel_order=neopixel.GRB
)

# --- Define colors ---
colors = [
    (255, 0, 0),   # Red
    (0, 255, 0),   # Green
    (0, 0, 255),   # Blue
    (255, 255, 255),  # White
    (0, 0, 0)      # Off
]

# --- Main loop ---
while True:
    for color in colors:
        pixels.fill(color)  # set all LEDs
        pixels.show()
        time.sleep(1)       # hold for 1 second
