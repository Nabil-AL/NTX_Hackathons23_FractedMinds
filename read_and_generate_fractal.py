from pylsl import StreamInlet, resolve_stream
import pygame
from utils import generate_live_fractal


def main():
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream('name', 'openvibeSignal')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

    generate_live_fractal(pygame, inlet)


if __name__ == '__main__':
    main()