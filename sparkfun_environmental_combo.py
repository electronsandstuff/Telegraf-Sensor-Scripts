import json
import time
from qwiic_bme280 import QwiicBme280
from qwiic_ccs811 import QwiicCcs811


if __name__ == '__main__':
    # Launch the drivers
    bme = QwiicBme280()

    # Double check that the sensors are connected correctly
    if not bme.is_connected():
        raise ValueError('BME sensor was not detected')

    # Start the drivers
    bme.begin()
    bme.set_mode(bme.MODE_SLEEP)
    time.sleep(1)  # Give it a second before we read data

    # Read the data and dump to json output
    bme.set_mode(bme.MODE_FORCED)  # Run one measurement
    print(json.dumps({
        'pressure': bme.read_pressure(),
        'humidity': bme.read_humidity(),
        'temp': bme.get_temperature_celsius(),
        #'tvoc': ccs.get_tvoc(),
        #'co2_ccs811': ccs.get_co2(),
    }))

    # Put BME280 to sleep
    bme.set_mode(bme.MODE_SLEEP)
