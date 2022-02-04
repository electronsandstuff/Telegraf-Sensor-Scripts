from pms5003 import PMS5003


device = '/dev/ttyUSB0'


if __name__ == '__main__':
    pms = PMS5003(device=device, baudrate=9600)
    print(pms.read().as_influxdb_line_proto())
