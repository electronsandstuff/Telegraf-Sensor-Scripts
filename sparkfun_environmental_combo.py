import json
import time
from patched_bm280_driver import QwiicBme280
from qwiic_ccs811 import QwiicCcs811


# Some constants
bme280_sleep_time = 0.5  # How long to wait after starting BME280
ccs811_sleep_time = 2  # How long to wait after starting CCS811


if __name__ == '__main__':
    # Launch the BME280 driver
    bme = QwiicBme280()
    if not bme.is_connected():
        raise ValueError('BME280 sensor was not detected')
    bme.begin()
    time.sleep(bme280_sleep_time)

    # Get values from bme280
    sensor_vals = {
        'temperature': bme.get_temperature_celsius(),  # Must be called first due to quirks in the sparkfun library
        'humidity': bme.read_humidity(),
        'pressure': bme.read_pressure(),
    }

    # Launch the CCS811 driver
    ccs = QwiicCcs811()
    if not ccs.is_connected():
        raise ValueError('CCS811 sensor was not detected')
    err = ccs.begin()
    if err != ccs.SENSOR_SUCCESS:
        raise RuntimeError(f'CCS811 could not be initialized, begin returned {err}')
    err = ccs.set_environmental_data(sensor_vals['humidity'], sensor_vals['temperature'])
    if err != ccs.SENSOR_SUCCESS:
        raise RuntimeError(f'Could not set CCS811 temp/humidity calibration, method returned {err}')
    time.sleep(ccs811_sleep_time)

    # Read sensor values
    print(ccs.data_available())
    ccs.read_algorithm_results()
    sensor_vals['tvoc'] = ccs.get_tvoc()
    sensor_vals['co2_ccs811'] = ccs.get_co2()

    # Dump the data to STDOUT
    print(json.dumps(sensor_vals))
