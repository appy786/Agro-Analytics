from plantcv import sim as ps
from plantcv import qgc
import time
ps.sitl()
if 1:
    time.sleep(5)
ps.mavproxy()
if 1:
    time.sleep(10)
qgc.qground()
if 1:
     time.sleep(15)
sim.kill()

