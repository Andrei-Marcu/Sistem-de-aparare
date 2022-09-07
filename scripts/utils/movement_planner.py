import time
import numpy
import serial

from utils.functions import *
from threading import Lock
from config import *

ready = Lock()
currentPos = [0, 0]


s = serial.Serial("COM5", baud_rate)


def send_locking(command):
    s.write((command + '\n').encode())
    while True:
        response = s.read_until()
        if response == b'ok\n':
            break
        else:
            print(response.decode("utf-8"), end="")


def flush():
    s.flushInput()


def dwell():
    send_locking("M400")


def home():
    global ready
    ready.acquire()
    time.sleep(sleep_secs)
    flush()
    send_locking("G0 F" + speed)
    # send_locking("G28 X Y")
    # dwell()
    send_locking("G92 X0 Y0")
    ready.release()


runasync(home)


def try_move(pos):
    global ready
    if not ready.locked():
        def move_locking():
            global ready, currentPos
            ready.acquire()

            targetpos = [round(numpy.clip(pos[0], currentPos[0] - delta, currentPos[0] + delta), 2),
                         round(numpy.clip(pos[1], currentPos[1] - delta, currentPos[1] + delta), 2)]
            dwell()
            send_locking("G0 X" + str(targetpos[0]) + " Y" + str(targetpos[1]))
            currentPos = targetpos
            ready.release()

        runasync(move_locking)


def toggle_splash(splashing):
    def splash_locking():
        global ready
        ready.acquire()
        send_locking("M106 S" + splash_power if splashing else "M107")
        ready.release()
    runasync(splash_locking)
