from tkinter import *
import tkinter.font
from gpiozero import LED
import RPi.GPIO

RPi.GPIO.setmode(RPi.GPIO.BCM)

## hardware
red = LED(13)
green = LED(26)
blue = LED(19)

## GUI DEFINITIONS ##

win = Tk()
win.title("RGB led toggler")
myFont = tkinter.font.Font(family='Helvetica', size=12, weight="bold")

# Keep track of the currently active LED
current_led = None

### EVENT FUNCTION###

def toggle_led(led, button):
    global current_led
    if current_led is not None:
        current_led.off()
        current_led = None
    
    if led.is_lit:
        led.off()
        button["text"] = "Turn {} LED On".format(button["bg"])
    else:
        led.on()
        current_led = led
        button["text"] = "Turn {} LED Off".format(button["bg"])

def close():
    RPi.GPIO.cleanup()
    win.destroy()

### WIDGETS ###

# Create buttons for each LED
led_buttons = []

for color, pin in [("Red", red), ("Green", green), ("Blue", blue)]:
    button_text = "Turn {} LED On".format(color)
    button = Button(win, text=button_text, font=myFont, 
                    command=lambda pin=pin, button_text=button_text: toggle_led(pin, button), 
                    bg=color.lower(), height=1, width=24)
    button.grid(row=len(led_buttons), column=1)
    led_buttons.append(button)

win.protocol("WM_DELETE_WINDOW", close)

# Ensure all LEDs are initially turned off
red.off()
green.off()
blue.off()

win.mainloop()
