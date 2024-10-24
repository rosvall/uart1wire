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
    DEV                Path to uart device
    CMD is one of:
    -v                 Toggle verbose mode (default off)
    -b                 Toggle raw binary output from reads (default off)
    -R                 Perform bus reset
    -w HEX [HEX ...]   Write bytes to bus
    -r COUNT           Read COUNT bytes from bus
    -r FMT             Read from bus and parse as python struct format string FMT

    Example:
    ./uart1wire.py /dev/ttyUSB0 -v -R -w 33 -r 8
```

## How do i hook it up?
![Simple schematic](https://github.com/user-attachments/assets/1dd2ca68-75c6-438a-ba91-649aebd86248)

## Notes
### Captured waveform for the curious
![waveform](https://github.com/user-attachments/assets/4f637ada-3d7d-480b-958b-346bf0def793)
Transmitting a 0x33 byte to a 1-wire device.
