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
        'temperature': bme.get_temperature_celsius(),  # Must be called first due to quirks in the sparkfun library
        'humidity': bme.read_humidity(),
        'pressure': bme.read_pressure(),
    }
    bme.set_mode(bme.MODE_SLEEP)  # Put the BME280 to sleep until next time

    # Dump the data to STDOUT
    print(json.dumps(sensor_vals))
