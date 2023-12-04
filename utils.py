import serial
import time
from math import cos, sin, pi
import random


def get_substring_between_flags(text, flag1, flag2):
    """
    :param text:
    :param flag1:
    :param flag2:
    :return:
    """
    start = text.find(flag1)
    if start == -1:
        return None
    end = text.find(flag2, start + len(flag1))
    if end == -1:
        return None
    return text[start + len(flag1):end]


def read_serial_data(data_queue, outlet, SERIAL_PORT, BAUD_RATE, DATA_RATE):
    """
    Function to handle data reading from the serial port.
    :param data_queue:
    :param outlet:
    :param SERIAL_PORT:
    :param BAUD_RATE:
    :param DATA_RATE:
    :return:
    """
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        while True:
            v=b'\x0c'
            # print(v)
            a = ser.write(v)
            # print(a)
            data = ser.read(2)
            value = int.from_bytes(data,byteorder="little", signed=False)
            # valfloat = (value-500)/1024.  # Scale the 10 bits value sent by Arduino board between -1 and 1
            outlet.push_sample([value])

            # print(data,value)
            data_queue.append(value)
            time.sleep(1.0 / DATA_RATE)


def update(data_queue, line, axe, MAX_POINTS):
    """
    This function is called periodically from FuncAnimation
    :return: (tuple)
    """
    if data_queue:
        # Update data for plot
        y_data = list(data_queue)
        x_data = range(len(y_data))

        # Update plot data
        line.set_data(x_data, y_data)
        axe.set_xlim(0, MAX_POINTS)
        axe.set_ylim(min(y_data)-10, max(y_data)+10)

    return line,


def generate_live_fractal(pygame, inlet):
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    running = True

    palettes = [
        [0x35f900, 0x72f000, 0x97e600, 0xb5db00, 0xcecf00, 0xe5c100, 0xf9b300, 0xffa300, 0xff9100, 0xff7e00, 0xff6900, 0xff5027, 0xff3043, 0xff005a, 0xff0072, 0xff0088, 0xff009f, 0xff00b5, 0xff00cb, 0xf900df, 0xff00cb, 0xff00b5, 0xff009f, 0xff0088, 0xff0072, 0xff005a, 0xff3043, 0xff5027, 0xff6900, 0xff7e00, 0xff9100, 0xffa300, 0xf9b300, 0xe5c100, 0xcecf00, 0xb5db00, 0x97e600, 0x72f000, 0x35f900],
        [0xff0000, 0xff3400, 0xff4e00, 0xff6300, 0xff7500, 0xff8700, 0xff9700, 0xffa700, 0xffb600, 0xffc500, 0xffd400, 0xffe300, 0xfff100, 0xfcff00, 0xfcff00, 0xfeff35, 0xffff4e, 0xffff62, 0xffff75, 0xffff85, 0xffff96, 0xffffa5, 0xffffb5, 0xffffc4, 0xffffd3, 0xffffe1, 0xfffff0, 0xffffff, 0xd7d7d6, 0xb1b1af, 0x8c8c89, 0x696965, 0x484843, 0x292924, 0x0a0a00, 0x210101, 0x470911, 0x740517, 0xa20019, 0xd00014, 0xff0000],
        [0x4157e2, 0x0064eb, 0x0070f1, 0x007af5, 0x0083f7, 0x008bf6, 0x0093f3, 0x009aef, 0x00a1ea, 0x00a7e3, 0x00addc, 0x00b3d4, 0x00b8cd, 0x00bdc5, 0x00c2be, 0x00c6b8, 0x39cab2, 0x5bceae, 0x74d2ab, 0x89d5a9, 0x74d2ab, 0x5bceae, 0x39cab2, 0x00c6b8, 0x00c2be, 0x00bdc5, 0x00b8cd, 0x00b3d4, 0x00addc, 0x00a7e3, 0x00a1ea, 0x009aef, 0x0093f3, 0x008bf6, 0x0083f7, 0x007af5, 0x0070f1, 0x0064eb, 0x4157e2]
    ]
    palette_index = 0

    # colors = [0x4727eb, 0x0043f0, 0x0054f0, 0x0060ec, 0x0069e3, 0x0071d8, 0x0076cb, 0x007bbd, 0x007faf, 0x0082a2,
    # 0x0087a3, 0x008ba2, 0x00909e, 0x009498, 0x00978e, 0x009a83, 0x009d74, 0x009f64, 0x00a152, 0x00a23d, 0x2ca93b,
    # 0x43b138, 0x56b835, 0x68bf32, 0x7ac62f, 0x8bcd2c, 0x9cd328, 0xaeda25, 0xbfe022, 0xd1e620, 0xd8da0b, 0xddcf00,
    # 0xe2c300, 0xe5b700, 0xe8ab00, 0xea9f00, 0xea9300, 0xea870d, 0xe87b18, 0xe66f20, 0xed652c, 0xf45939, 0xf94e45,
    # 0xfc4152, 0xfe3560, 0xfd286e, 0xfb1d7d, 0xf7168d, 0xf0189c, 0xe620ac, 0xdb32b8, 0xce3fc3, 0xc04bcc, 0xb054d4,
    # 0x9f5ddb, 0x8d64e0, 0x796be4, 0x6270e6, 0x4875e7, 0x2079e6, 0x2079e6, 0x008df7, 0x009efd, 0x00aef9, 0x00bbea,
    # 0x00c7d2, 0x00d1b3, 0x00da90, 0x00e16c, 0x7fe547, 0xbee620, 0xc9d600, 0xd3c600, 0xdbb600, 0xe1a400, 0xe69300,
    # 0xea8000, 0xeb6d00, 0xeb5800, 0xea400f, 0xe62020, 0xe62020, 0xe94f49, 0xe7716e, 0xdf8f8f, 0xde8590, 0xdc7c94,
    # 0xd87499, 0xd26ca0, 0xc966a8, 0xbd62b1, 0xad5fba, 0x995ec4, 0x7e5fcd, 0x5861d5, 0x1b72df, 0x0080e3, 0x008ce3,
    # 0x0097df, 0x00a1d7, 0x00aace, 0x00b1c5, 0x1eb8bc, 0x52beb5, 0x73c4b0, 0x73c4b0, 0x5ec0bc, 0x4fbcc8, 0x4ab6d3,
    # 0x53afda, 0x66a6dc, 0x7e9dda, 0x9592d2, 0xa987c5, 0xb97cb3, 0xc4739d, 0xc4739d, 0xd37997, 0xe08091, 0xea898a,
    # 0xf19384, 0xf59f7f, 0xf6ac7b, 0xf5b97a, 0xf1c77c, 0xebd482, 0xe3e28b, 0xeeecb2, 0xf7f5d8, 0xffffff, 0xcccccc,
    # 0x9b9b9b, 0x6d6d6d, 0x424242, 0x3b3b3b, 0x343434, 0x2d2d2d, 0x272727, 0x202020, 0x1a1a1a, 0x141414, 0x0b0b0b,
    # 0x000000, 0x0d0922, 0x0f1239, 0x101850, 0x121d69, 0x162183, 0x1d249c, 0x2827b7, 0x3628d1, 0x4727eb]

    start = random.randrange(len(palettes[0]))
    while True:
        print("Sample receiving started")

        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        print(timestamp, sample)

        print("Sample receiving ended")

        min_re = min_im = -2.0
        max_re = max_im = 2.0
        max_iter = 400

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                palette_index = (palette_index + 1) % len(palettes)
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        if not running:
            break

        print("Fractal calculation started")
        # iterate over each pixel to compute the fractal
        time = pygame.time.get_ticks() / 1000.0
        turns = time / 4
        start += random.randrange(4, 10)
        colors = palettes[palette_index]
        for i in range(screen.get_height()):
            for j in range(screen.get_width()):
                c = (sample[0] / 300.0 * 0.1 + 0.78) * (cos(turns * 2 * pi) + 1j * sin(turns * 2 * pi))
                z = (
                        min_re + (j * (max_re - min_re) / screen.get_width())
                        + 1j * (min_im + (i * (max_im - min_im) / screen.get_height()))
                )
                for step in range(max_iter):
                    if z.real * z.real + z.imag * z.imag > 4:
                        color_index = (start + step * 2) % len(colors)
                        screen.set_at((j, i), colors[color_index])
                        break
                    z = z * z + c
                else:
                    screen.set_at((j, i), (0, 0, 0))

        # flip() the display to put your work on screen
        pygame.display.flip()
        print("Fractal calculation ended")

        clock.tick(60)  # limits FPS to 60

    pygame.quit()
