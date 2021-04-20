from subprocess import call
import time
import os
import signal
def sitl():
	print("Start simulator (SITL)")
	print("Starting sketch 'ArduCopter'")
	print("Serial port 0 on TCP port 5760")
	print("Starting SITL input")
	call(['gnome-terminal', '-e', "dronekit-sitl copter"])
	print("Waiting for connection with ground station(MAVProxy) ....")

def goto():
	call(['gnome-terminal', '-e', "python3 goto.py --connect 127.0.0.1:14551"])
	
def mavproxy():
	call(['gnome-terminal', '-e', "mavproxy.py --master tcp:127.0.0.1:5760 --sitl 127.0.0.1:5501 --out 127.0.0.1:14550 --out 127.0.0.1:14551"])
	print("SITL is safely connected with MAVProxy")
	print("Waiting for connection with ground station(QGC) ....")
	
def qgc():
	call(['gnome-terminal', '-e', "python3 qgc.py"])
	print("SITL is safely connected with QGC")
	print("Drone is ready to fly....")

	


def kill():
	os.kill(os.getppid(), signal.SIGHUP)
