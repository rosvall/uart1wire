# Python 1-wire over serial tool/library
Use it to talk to your OneWire stuff using nothing but a USB to TTL serial adapter, a resistor, and a diode.

## Requirements
* [pyserial](https://pypi.org/project/pyserial/)
* Some sort of serial adapter with 3.3 or 5V TTL input/output - NOT a regular serial port that outputs RS232 levels.

## API
### Example usage
```python
import uart1wire
bus = uart1wire.OneWire('/dev/ttyUSB0')
bus.reset()
bus.write(bytes([0x33]))
rom_id = bus.read(8)
```

### `OneWire.__init__(dev: str)`
You can pass options to the pyserial constructor if you feel like tweaking something. 

### `OneWire.reset()`
Perform a bus reset, check for device presence. Raises `NoPresence` if no device responds.

### `OneWire.write(data: bytes)`
Transmit bytes on bus. Raises `Collision` if there is a collision.

### `OneWire.read(count: int)`
Reads `count` bytes from bus. Raises `SymbolError` if a device holds the bus low for too long.

## Use as stand-alone tool
```
USAGE:
    ./uart1wire.py DEV CMD [CMD ...]
    DEV                 Path to uart device
    CMD is one of:
    -v                  Toggle verbose mode (default off)
    -b                  Toggle raw binary output from reads (default off)
    reset               Perform bus reset
    write HEX [HEX ...] Write bytes to bus
    read COUNT          Read COUNT bytes from bus
    read FMT            Read from bus and parse as python struct format string FMT
    -I                  Enter interactive console

    Example:
    ./uart1wire.py /dev/ttyUSB0 -v reset write 33 read 8
```

## How do i hook it up?
![Schematic](https://github.com/user-attachments/assets/cdd006d3-66b1-4124-bb5e-5c24d50b9938)

## Notes
### Captured waveform for the curious
![waveform](https://github.com/user-attachments/assets/4f637ada-3d7d-480b-958b-346bf0def793)
Transmitting a 0x33 byte to a 1-wire device.
