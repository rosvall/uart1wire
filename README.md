# Python 1-wire over serial tool/library
Use it to talk to your OneWire stuff using nothing but a USB to TTL serial adapter, a resistor, and a diode.

### How do i hook that up?
![schem](https://github.com/user-attachments/assets/0e27fdda-df21-40c5-bc37-b77b72f7920f)

### This is what it looks like when sending the byte 0x33 to a 1-wire device
![write0x33](https://github.com/user-attachments/assets/4f637ada-3d7d-480b-958b-346bf0def793)

## API usage example
```python
import uart1wire
bus = uart1wire.OneWire('/dev/ttyUSB0')
bus.reset()
bus.write(bytes([0x33]))
rom_id = bus.read(8)
```

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
