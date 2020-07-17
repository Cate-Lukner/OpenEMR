import subprocess
import signal
import os

filename="./sample4.pdf"
plot = subprocess.Popen("xdg-open '%s'" % filename, shell=True)

input("test")
os.killpg(os.getpgid(plot.pid), signal.SIGTERM)