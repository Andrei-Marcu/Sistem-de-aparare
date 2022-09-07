import cv2
import math

from config import *
from threading import Thread


def setrez(cp):
    cp.set(6, codec)
    cp.set(5, fps)
    cp.set(3, frameSize[0])
    cp.set(4, frameSize[1])


def runasync(func):
    t = Thread(target=func)
    t.setDaemon(True)
    t.start()
    return t


def select(aList, fun):
    return list(map(fun, aList))


def stringifypos(pos):
    pos /= 10
    return str(round(pos[0][0], 1)) + " " + str(round(pos[1][0], 1)) + " " + str(round(pos[2][0], 1))


def convert_pos(pos):
    x, z, y = pos
    x, z = -x, -z

    d = math.sqrt(x * x + y * y)

    dprime = math.sqrt(d * d - r * r)

    sigma = math.degrees(math.atan(x / y) - math.asin(r / d))

    incline = math.degrees(math.atan(z / dprime))

    return [sigma, incline]
