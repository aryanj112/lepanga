"""Keyboard jog control — one increase/decrease key pair per servo.

  g / h  shoulder_pan   increase / decrease
  r / t  shoulder_lift  increase / decrease
  y / u  elbow_flex     increase / decrease
  i / o  wrist_flex     increase / decrease
  k / l  wrist_roll     increase / decrease
  n / m  gripper        increase / decrease

Ctrl+C to quit.
"""

from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode
import sys
import termios
import tty
import os

PORT = "/dev/tty.usbmodem5B415321151"

motors = {
    "shoulder_pan":  Motor(1, "sts3215", MotorNormMode.RANGE_0_100),
    "shoulder_lift": Motor(2, "sts3215", MotorNormMode.RANGE_0_100),
    "elbow_flex":    Motor(3, "sts3215", MotorNormMode.RANGE_0_100),
    "wrist_flex":    Motor(4, "sts3215", MotorNormMode.RANGE_0_100),
    "wrist_roll":    Motor(5, "sts3215", MotorNormMode.RANGE_0_100),
    "gripper":       Motor(6, "sts3215", MotorNormMode.RANGE_0_100),
}

STEP = 20  # ticks per keypress

# key -> (motor name, direction)
KEYMAP = {
    "g": ("shoulder_pan", +1),
    "h": ("shoulder_pan", -1),
    "r": ("shoulder_lift", +1),
    "t": ("shoulder_lift", -1),
    "y": ("elbow_flex", +1),
    "u": ("elbow_flex", -1),
    "i": ("wrist_flex", +1),
    "o": ("wrist_flex", -1),
    "k": ("wrist_roll", +1),
    "l": ("wrist_roll", -1),
    "n": ("gripper", +1),
    "m": ("gripper", -1),
}


def read_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


bus = FeetechMotorsBus(port=PORT, motors=motors)
bus.connect()

for name in motors:
    bus.enable_torque(name)

positions = {name: bus.read("Present_Position", name, normalize=False) for name in motors}


def render():
    os.system("clear")
    print(__doc__)
    for name, pos in positions.items():
        print(f"{name:<15} {pos:>6}")


render()

try:
    while True:
        key = read_key()
        entry = KEYMAP.get(key)
        if entry is None:
            continue
        name, direction = entry
        target = max(0, min(4095, positions[name] + direction * STEP))
        bus.write("Goal_Position", name, target, normalize=False)
        positions[name] = target
        render()

except KeyboardInterrupt:
    print("\nStopped.")

finally:
    for name in motors:
        try:
            bus.disable_torque(name)
        except RuntimeError as e:
            print(f"Warning: failed to disable torque on {name}: {e}")
    bus.disconnect()
    print("Done, torque disabled.")
