#!/usr/bin/env python3

import psutil
import subprocess
import time
from gpiozero import Button, LED
from signal import pause
from subprocess import DEVNULL


def process_kill(process_name: str):
	for process in psutil.process_iter():
		if process.name() == process_name:
			process.kill()


def button_dispatch(action: str):
	power_led.blink()
	print(action)
	process_kill('ludo')
	time.sleep(2)
	subprocess.Popen([action], stdout=DEVNULL, stderr=DEVNULL)


def safe_reboot():
	button_dispatch('reboot')


def safe_poweroff():
	button_dispatch('poweroff')


if __name__ == "__main__":
	POWER = 3
	RESET = 2
	POWER_LED = 14

	power_button = Button(POWER)
	reset_button = Button(RESET, hold_time=1)
	power_led = LED(POWER_LED)
	power_led.on()

	reset_button.when_held = safe_reboot
	power_button.when_pressed = safe_poweroff
	pause()
