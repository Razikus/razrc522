# razrc522

Modern Python library for RC522 RFID reader - updated for current Python and kernel versions 6+

## About

This is a modernized repository of the original [pi-rc522](https://github.com/ondryaso/pi-rc522) library with significant improvements:

- **Modern GPIO handling** - Rewritten to use current `gpiozero` and `lgpio` libraries instead of deprecated RPi.GPIO
- **Simplified API** - Easy-to-use `EasyRFID` wrapper class for common operations
- **Multiple UID formats** - Support for various UID output modes (HEX, decimal, binary, base64, etc.)
- **IRQ support** - Optimized for RC522 modules with interrupt pin for efficient tag detection
- **Python 3.7+ compatibility** - Updated for modern Python versions
- **Kernel 6+ support** - Works with latest Raspberry Pi OS releases and Compute Module 4/5
- **Better error handling** - Simple boolean returns instead of complex error tuples like original's `(error, data, length)`
- **Production ready** - Designed for real-world applications, not just prototypes 

## Hardware Compatibility

This library is specifically designed for RC522 RFID modules with IRQ pin support. 

### Recommended Hardware

**[Compute Module 4/5 Production Base Board with RFID](https://shop.razniewski.eu/products/compute-module-4-5-production-base-board-with-rfid-hdmi-usb-rtc)** - Professional development board specifically designed for RFID applications:

**Hardware Features:**
- **Dedicated SPI RFID connector** - TE Connectivity 3-640621-8 with all required lines (MISO, MOSI, SCK, SDA, IRQ, RST, 3V3, GND)
- **No wiring required** - Direct plug-and-play compatibility with RC522 modules
- **Production-grade components** - 100Mb/s Ethernet, USB-C power, HDMI output, RTC with battery backup
- **Compact design** - 64.5×92.6×15.2mm, perfect for enclosure mounting
- **Built-in signaling** - Buzzer and programmable GPIO for status indication

**Software Integration:**
- **Perfect pin mapping** - Default configuration matches this library exactly
- **Sample applications included** - REST API software for immediate deployment
- **CM4/5 eMMC support** - Industrial-grade storage for production applications

**Ideal Use Cases:**
- Access control and time registration systems
- IoT devices with RFID authentication
- Industrial terminals and kiosks
- Prototype-to-production development

*While this library works with any RC522 setup, the above board eliminates wiring complexity and provides a complete hardware platform for professional RFID applications.*

### Default Pin Configuration
- RST: GPIO 22
- CE: GPIO 0 (CE0)
- IRQ: GPIO 18
- SPI: Default SPI0 (MOSI=GPIO 10, MISO=GPIO 9, SCLK=GPIO 11)

## Installation

```bash
pip install razrc522
```

## Quick Start

### Simple UID Reading

```python
from razrc522.rfid import RFID
from razrc522.easyrfid import EasyRFID, EasyRFIDUIDMode

# Initialize reader
reader = RFID()
easy_rfid = EasyRFID(reader, mode=EasyRFIDUIDMode.HEX)

# Read UID in different formats
while True:
    uid = easy_rfid.wait_and_read_uid()
    print(f"Card UID: {uid}")
```

### Reading and Writing Data

```python
from razrc522.rfid import RFID
from razrc522.easyrfid import EasyRFID, EasyRFIDUIDMode, EasyRFIDAuth

reader = RFID(antenna_gain=7)
easy_rfid = EasyRFID(reader, mode=EasyRFIDUIDMode.HEX)

while True:
    # Wait for card and select it
    uid, raw_uid = easy_rfid.wait_and_select()
    print(f"Selected card: {uid}")
    
    # Authorize with default MIFARE key
    block = 8
    if easy_rfid.authorize(EasyRFIDAuth.AuthB, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], raw_uid, block):
        # Read block
        data = easy_rfid.read_block(block)
        if data:
            text = easy_rfid.bytes_to_uid(data, EasyRFIDUIDMode.STRING)
            print(f"Block {block} contains: {text}")
            
        # Write data (16 bytes required)
        message = b"Hello RFID World!"[:16].ljust(16, b'\x00')
        if easy_rfid.write_block(block, message):
            print("Write successful!")
```

## UID Output Modes

The `EasyRFIDUIDMode` enum supports various output formats:

- `HEX` - Hexadecimal string (e.g., "a1b2c3d4")
- `HEX_BACKWARD` - Reversed hexadecimal
- `DECIMAL` - Decimal string
- `BINARY` - Binary string
- `BASE64` - Base64 encoded
- `INT_LIST` - List of integers (default)
- `STRING` - ASCII string representation
- `RAW` - Raw bytes object

```python
# Switch between modes dynamically
easy_rfid.set_new_mode(EasyRFIDUIDMode.DECIMAL)
uid_decimal = easy_rfid.wait_and_read_uid()

# Or convert existing data
hex_uid = easy_rfid.bytes_to_uid([161, 178, 195, 212], EasyRFIDUIDMode.HEX)
```

## Advanced Configuration

### Custom Pin Setup

```python
reader = RFID(
    bus=0,              # SPI bus
    device=0,           # SPI device
    speed=1000000,      # SPI speed
    pin_rst=22,         # Reset pin
    pin_ce=0,           # Chip enable pin
    pin_irq=18,         # Interrupt pin
    antenna_gain=7,     # Antenna gain (0-7)
    logger=None         # Custom logger
)
```

### Antenna Gain Settings

The antenna gain affects the reading range:

- 0: 18 dB
- 1: 23 dB
- 2: 18 dB
- 3: 23 dB
- 4: 33 dB (default)
- 5: 38 dB
- 6: 43 dB
- 7: 48 dB (maximum range)

## Examples

See the `examples/` directory for complete working examples:

- `read_uid_modes.py` - Demonstrates all UID output modes
- `read_full_0.py` - Reading card data with authentication
- `write.py` - Writing data to cards with random content

## Requirements

- Python 3.7+
- Raspberry Pi with SPI enabled
- RC522 RFID module with IRQ pin connected
- Linux kernel 6+ (for modern GPIO support)

## Dependencies

- `gpiozero==2.0.1` - Modern GPIO control
- `spidev==3.7` - SPI communication
- `lgpio==0.2.2.0` - Low-level GPIO access

## License

MIT License - see LICENSE file for details.

## Contributing

Issues and pull requests welcome! This library aims to provide a simple, modern interface for RC522 RFID operations on Raspberry Pi.

## Credits

- Original [pi-rc522](https://github.com/ondryaso/pi-rc522) by Ondřej Ondryáš
- Modernized and extended by Adam Raźniewski

---

*For more hardware solutions and Raspberry Pi accessories, visit [razniewski.eu](https://shop.razniewski.eu)*