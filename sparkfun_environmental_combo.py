import qwiic
import json
import time


if __name__ == '__main__':
    bme = qwiic.QwiicBme280()
    ccs = qwiic.QwiicCcs811()

    if not bme.is_connected():
        raise ValueError('BME sensor was not detected')
    if not ccs.is_connected():
        raise ValueError('CCS811 sensor was not detected')

    bme.begin()
    ccs.begin()
    ccs.read_algorithm_results()
    time.sleep(1)

    print(json.dumps({
        'pressure': bme.get_reference_pressure(),
        'altitude': bme.get_altitude_meters(),
        'humidity': bme.read_humidity(),
        'temp': bme.get_temperature_celsius(),
        'dew': bme.get_dewpoint_celsius(),
        'tvoc': ccs.get_tvoc(),
        'co2_ccs811': ccs.get_co2(),
    }))
