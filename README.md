# Generate live piece of art with brain waves and using the cheapest EEG recorder

## Order of files to be run


1) ‘ArduinoReadSerial.ino’ to listen to the signal and print its state out of the board


2) ‘stream_push.py’ with pylsl to transfer the signal to Lab Streaming Layer (LSL)


3) Use ‘openvibe_file.xml’ to acquire the signal in OpenVibe using LSL and apply preprocessing on it: resampling (256 Hz), pass-band filter (8-14 Hz) to extract the alpha band then average it to obtain one metric to use for the fractal. Finally export it using LSL.


4) Run ‘read_and_generate_fractal.py’ to read the metric and use it as a parameter to generate the live Fractal.


## Demo Video link

https://streamable.com/b2none