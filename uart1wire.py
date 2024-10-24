#!/bin/python
"""
Very simple implementation of 1-wire over uart.
"""

import serial


class BusError(Exception):
    pass

class NoPresence(BusError):
    pass

class SymbolError(BusError):
    pass

class Collision(BusError):
    pass



def bits_lsb_first(byte):
    for i in range(8):
        yield (byte >> i) & 1

def bit_pattern(data: bytes):
    SINGLE_BIT_PATTERN = 0x80, 0xFF
    for byte in data:
        for bit in bits_lsb_first(byte):
            yield SINGLE_BIT_PATTERN[bit]


class OneWire:
    def __init__(self, dev: str, baudrate=115200, timeout=0.01, **kwargs):
        self._uart = serial.Serial(port=dev, baudrate=baudrate, timeout=timeout, **kwargs)

    def reset(self):
        RESET_PATTERN = 0xF0
        "Perform bus reset with presence detection"
        saved_baudrate = self._uart.baudrate
        self._uart.baudrate = 9600
        self._uart.write([RESET_PATTERN])
        on_bus = self._uart.read(1)[0]
        self._uart.baudrate = saved_baudrate
        if on_bus == RESET_PATTERN:
            raise NoPresence('Did not receive presence detect pulse after reset')

    def write(self, data: bytes):
        bits = bytes(bit_pattern(data))
        self._uart.write(bits)
        on_bus = self._uart.read(len(bits))
        if bits != on_bus:
            raise Collision(f'Wrote: {bits.hex()}\nOn bus: {on_bus.hex()}')

    def _rx_single_byte(self):
        byte = 0
        for i in range(8):
            self._uart.write([0xff])
            pattern = self._uart.read(1)[0]
            if pattern & 0xf0 != 0xf0:
                raise SymbolError('Bus held low for too long')
            bit = pattern & 1
            byte |= bit << i
        return byte

    def read(self, count: int):
        return bytes(self._rx_single_byte() for _ in range(count))


if __name__ == '__main__':
    import sys
    import struct

    USAGE = f"""USAGE:
    {sys.argv[0]} DEV CMD [CMD ...]
    DEV                Path to uart device
    CMD is one of:
    -v                 Toggle verbose mode (default off)
    -b                 Toggle raw binary output from reads (default off)
    -R                 Perform bus reset
    -w HEX [HEX ...]   Write bytes to bus
    -r COUNT           Read COUNT bytes from bus
    -r FMT             Read from bus and parse as python struct format string FMT

    Example:
    {sys.argv[0]} /dev/ttyUSB0 -v -R -w 33 -r 8
    """

    def errout(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    if len(sys.argv) < 3:
        errout(USAGE)
        exit(-1)

    _, dev, *args = sys.argv

    ow = OneWire(dev)

    commands = '-b', '-v', '-r', '-w', '-R'

    verbose = False
    binary = False

    while args:
        cmd = args.pop(0)
        if cmd == '-v':
            verbose = not verbose
        elif cmd == '-b':
            binary = not binary
        elif cmd == '-R':
            if verbose:
                errout('reset')
            ow.reset()
        elif cmd == '-w':
            data = b''
            while args and args[0] not in commands:
                data += bytes.fromhex(args.pop(0))
            ow.write(data)
            if verbose:
                errout('write:', data.hex(' '))
        elif cmd == '-r':
            fmt_or_count = args.pop(0)
            fmt = None
            try:
                count = int(fmt_or_count)
            except ValueError:
                fmt = fmt_or_count
                count = struct.calcsize(fmt_or_count)
            data = ow.read(count)
            if verbose:
                errout(' read:', data.hex(' '))
            if binary:
                sys.stdout.buffer.write(data)
            else:
                if fmt:
                    print(*struct.unpack(fmt, data))
                else:
                    print(data.hex(' '))
        else:
            raise Exception(f'Invalid command: {cmd}')