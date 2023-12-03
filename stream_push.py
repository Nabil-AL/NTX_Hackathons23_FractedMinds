import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import struct
import threading
import time
import collections
from pylsl import StreamInfo, StreamOutlet, local_clock


#Serial port settings
SERIAL_PORT = 'COM5'  # Replace with your serial port
BAUD_RATE = 9600
DATA_RATE = 1000  # Data read frequency in Hz

#Plot settings
PLOT_UPDATE_RATE = 10  # Plot update frequency in Hz
MAX_POINTS = 200  # Max number of points to display on the plot

#Thread-safe queue for data
data_queue = collections.deque(maxlen=MAX_POINTS)

info = StreamInfo("nabilou", "eegt", 1, channel_format='float32')
# next make an outlet
outlet = StreamOutlet(info)
import re

def get_substring_between_flags(text, flag1, flag2):
  start = text.find(flag1)
  if start == -1:
    return None
  end = text.find(flag2, start + len(flag1))
  if end == -1:
    return None
  return text[start + len(flag1):end]
xmls = outlet.get_info().as_xml()
port = get_substring_between_flags(xmls,"<v4data_port>", "</v4data_port>")
print(port)

#Function to handle data reading from the serial port
def read_serial_data():
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        while True:
            v=b'\x0c'
            #print(v)
            a = ser.write(v)
            #print(a)
            data = ser.read(2)
            value = int.from_bytes(data,byteorder="little", signed=False)
            valfloat = (value-500)/1024.
            outlet.push_sample([valfloat])

            #print(data,value)
            data_queue.append(value)
            time.sleep(1.0 / DATA_RATE)

#Start the serial reading in a separate thread
thread = threading.Thread(target=read_serial_data, daemon=True)
thread.start()

#This function is called periodically from FuncAnimation
def update(frame):
    if data_queue:
        # Update data for plot
        y_data = list(data_queue)
        x_data = range(len(y_data))

        # Update plot data
        line.set_data(x_data, y_data)
        ax.set_xlim(0, MAX_POINTS)
        ax.set_ylim(min(y_data)-10, max(y_data)+10)

    return line,

#Create figure for plotting
fig, ax = plt.subplots()
line, = ax.plot([], [], 'r-')
ax.set_xlim(0, MAX_POINTS)
ax.set_ylim(0, 65535)  # Assuming uint16 data

#Set up plot to call update() function periodically
ani = FuncAnimation(fig, update, interval=1000. / PLOT_UPDATE_RATE, fargs=())

plt.show()