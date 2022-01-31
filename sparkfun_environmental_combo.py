from contextlib import contextmanager
import sys, os
import json
import time


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


# The qwiic library has some text output if optional packages arent' included. This suppresses it
with suppress_stdout():
    import qwiic


if __name__ == '__main__':
    # Launch the drivers
    bme = qwiic.QwiicBme280()
    ccs = qwiic.QwiicCcs811()

    # Double check that the sensors are connected correctly
    if not bme.is_connected():
        raise ValueError('BME sensor was not detected')
    if not ccs.is_connected():
        raise ValueError('CCS811 sensor was not detected')

    # Start the drivers
    bme.begin()
    ccs.begin()
    ccs.read_algorithm_results()
    time.sleep(1)  # Give it a second before we read data

    # Read the data and dump to json output
    print(json.dumps({
        'pressure': bme.read_pressure(),
        'humidity': bme.read_humidity(),
        'temp': bme.get_temperature_celsius(),
        'tvoc': ccs.get_tvoc(),
        'co2_ccs811': ccs.get_co2(),
    }))
