import serial
import struct
import json


serial_dev = '/dev/ttyS0'


def checksum(array):
    csum = sum(array) % 0x100
    if csum == 0:
        return struct.pack('B', 0)
    else:
        return struct.pack('B', 0xff - csum + 1)


if __name__ == '__main__':
    with serial.Serial(serial_dev, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                              stopbits=serial.STOPBITS_ONE, timeout=8.0) as ser:
        # Write to the sensor and read data back
        result = ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
        s = ser.read(9)

        # Check if data is valid
        if len(s) < 9:
            raise ValueError(f"Didn't receive enough bytes from device, requires 9, recieved {len(s)}")
        if s[0] != 0xff or s[1] != 0x86:
            raise ValueError(f"Start of device response is incorrect, recieved {s[0]} {s[1]}")
        if ord(checksum(s[1:-1])) != s[-1]:
            raise ValueError(f"Checksum was invalid, read value {s[-1]}, computed value {ord(checksum(s[1:-1]))}")

        # Convert to the actual sensor values
        sensor_vals = {
            'co2': float(s[2]*256 + s[3]),
            'temperature': float(s[4] - 40),
            'TT': float(s[4]),
            'SS': float(s[5]),
            'UhUl': float(s[6]*256 + s[7])
        }

    print(json.dumps(sensor_vals))
