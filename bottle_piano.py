import board
import busio
import usb_midi

import adafruit_midi
import adafruit_mpr121
import neopixel

from adafruit_debouncer import Button
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

i2c = busio.I2C(board.SCL1, board.SDA1)
mpr121 = adafruit_mpr121.MPR121(i2c)

buttons = [Button(mpr121[i], long_duration_ms=10) for i in range(12)]

pixels = neopixel.NeoPixel(board.A0, 150)

colors = [
    (0, 0, 255),
    (255, 0 ,255),
    (0, 255 ,0),
    (255, 0 ,0),
    (0, 255 ,255),
    (255, 0 ,255),
    (255, 0 ,255),
    (255, 0 ,255),
    (255, 0 ,255),
    (255, 0 ,255),
    (255, 0 ,255),
    (255, 0 ,255),
    ]

led_ranges = [
    (0, 16),
    (16,32),
    (32,48),
    (48,70),
    (70,109), #(0,31),
    (256,256),
    (256,256),
    (256,256),
    (256,256),
    (256,256),
    (256,256),
    (256,256),
    ]

pitches = [
    61,
    63,
    66,
    68,
    70,
    70,
    70,
    ]

playing = [False] * 12

modifier = 0

modifying = False

while True:
    for button in buttons:
        button.update()

    print(mpr121.touched_pins, modifier)
    for pad in range(len(pitches)):

        if mpr121.touched_pins[pad]:
            if not playing[pad]:
                pixels[led_ranges[pad][0]:led_ranges[pad][1]] = colors[pad] * (led_ranges[pad][1]-led_ranges[pad][0])
                midi.send(NoteOn(pitches[pad]+modifier, 127))
                playing[pad] = True
        else:
            pixels[led_ranges[pad][0]:led_ranges[pad][1]] = (0, 0, 0) * (led_ranges[pad][1]-led_ranges[pad][0])
            midi.send(NoteOff(pitches[pad]+modifier, 127))
            playing[pad] = False

    if buttons[11].released and not modifying:
        if modifier < 48:
            modifier = modifier + 12
            modifying = True
    else:
        modifying = False

    if buttons[10].released and not modifying:
        if modifier > -60:
            modifier = modifier - 12
            modifying = True
    else:
        modifying = False
