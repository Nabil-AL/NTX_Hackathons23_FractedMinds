"""
Read the data sent to the serial port and made available by AnalogReadSerial.ino (to run in Arduino Software).
In parallel (in another thread) send the data received to an LSL Stream.
The data received is displayed in a plot updated periodically
"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import collections
from pylsl import StreamInfo, StreamOutlet, local_clock
from utils import get_substring_between_flags, redirect_serial_data, update


# Serial port settings
SERIAL_PORT = 'COM5'  # Replace with your serial port (see Device Manager on Windows)
BAUD_RATE = 9600  # Should be the bit rate of your serial port
DATA_RATE = 1000  # Data read frequency in Hz

# Plot settings
PLOT_UPDATE_RATE = 10  # Plot update frequency in Hz
MAX_POINTS = 200  # Max number of points to display on the plot

# Create an LSL Stream
info = StreamInfo("nabilou", "eegt", 1, channel_format='float32')
# Next make an outlet
outlet = StreamOutlet(info)

# Code only to know the port number of the Stream
xmls = outlet.get_info().as_xml()
port = get_substring_between_flags(xmls, "<v4data_port>", "</v4data_port>")
print(port)

# Start the serial port reading in a separate thread and send the value received in the created outlet
data_queue = collections.deque(maxlen=MAX_POINTS)  # Thread-safe queue for data
target = redirect_serial_data(data_queue, outlet, SERIAL_PORT, BAUD_RATE, DATA_RATE)
thread = threading.Thread(target=target, daemon=True)
thread.start()

# Create figure for plotting
fig, ax = plt.subplots()
line, = ax.plot([], [], 'r-')
ax.set_xlim(0, MAX_POINTS)
ax.set_ylim(0, 65535)  # Assuming uint16 data

# Set up plot to call update() function periodically
update = update(data_queue, line, ax, MAX_POINTS)
ani = FuncAnimation(fig, update, interval=1000. / PLOT_UPDATE_RATE, fargs=())

plt.show()
