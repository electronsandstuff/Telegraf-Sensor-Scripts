import json
import time
from qwiic_bme280 import QwiicBme280
# from qwiic_ccs811 import QwiicCcs811


if __name__ == '__main__':
    # Launch the drivers
    bme = QwiicBme280()
    if not bme.is_connected():
        raise ValueError('BME sensor was not detected')
    bme.begin()
    time.sleep(1)

    # Get values from bme280
    sensor_vals = {
        'humidity': bme.read_humidity(),
        'pressure': bme.read_pressure(),  # NOTE: must be called after temp due to quirks in the sparkfun library
        'temp': bme.get_temperature_celsius()
    }
    bme.set_mode(bme.MODE_SLEEP)  # Put the BME280 to sleep until next time

    # Dump the data to STDOUT
    print(json.dumps(sensor_vals))
