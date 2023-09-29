# Import necessary modules
from tkinter import *
import tkinter.font
from gpiozero import LED
import RPi.GPIO

# Set the GPIO mode to BCM
RPi.GPIO.setmode(RPi.GPIO.BCM)

# Define hardware connections
red = LED(13)
green = LED(26)
blue = LED(19)

# Create the main GUI window
win = Tk()
win.title("RGB led toggler")
myFont = tkinter.font.Font(family='Helvetica', size=12, weight="bold")

# Keep track of the currently active LED
current_led = None

# Define the function to toggle an LED
def toggle_led(led, button):
    global current_led
    # If there is a currently active LED, turn it off
    if current_led is not None:
        current_led.off()
        current_led = None
    
    # Toggle the state of the selected LED
    if led.is_lit:
        led.off()
        button["text"] = "Turn {} LED On".format(button["bg"])
    else:
        led.on()
        current_led = led
        button["text"] = "Turn {} LED Off".format(button["bg"])

# Define a function to clean up GPIO and close the window
def close():
    RPi.GPIO.cleanup()
    win.destroy()

# Create a list to store LED buttons
led_buttons = []

# Create buttons for each LED (Red, Green, Blue)
for color, pin in [("Red", red), ("Green", green), ("Blue", blue)]:
    button_text = "Turn {} LED On".format(color)
    # Create a button with an associated command to toggle the LED
    button = Button(win, text=button_text, font=myFont, 
                    command=lambda pin=pin, button_text=button_text: toggle_led(pin, button), 
                    bg=color.lower(), height=1, width=24)
    button.grid(row=len(led_buttons), column=1)
    led_buttons.append(button)

# Set up a close event handler for the window
win.protocol("WM_DELETE_WINDOW", close)

# Ensure all LEDs are initially turned off
red.off()
green.off()
blue.off()

# Start the GUI main loop
win.mainloop()
