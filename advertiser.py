# Use this code to advertise data on the LEGO SPIKE Prime

from BLE_CEEO import Yell
from machine import ADC, Pin
import time

adc = ADC(Pin(27))  # Initialize ADC on GPIO pin 27
uvs = []


def get_voltage(value):
    ref = 3.3
    voltage = (value / 65535) * ref
    return voltage


def get_illumination(voltage):
    return voltage * 307


def get_uvindex(illumination):
    return illumination / 35


def measure_uv_index():
    value = adc.read_u16()
    voltage = get_voltage(value)
    illumination = get_illumination(voltage)
    uv_index = get_uvindex(illumination)
    return uv_index


def peripheral(name):
    x = 1
    try:
        p = Yell(name, verbose=True)
        if p.connect_up():
            print('P connected')
            time.sleep(2)
            while x < 10:
                uv_index = measure_uv_index()
                uv_index = round(uv_index, 2)
                payload = str(uv_index) + '\n'
                print(payload)
                p.send(payload)
                if p.is_any:
                    print(p.read())
                if not p.is_connected:
                    print('lost connection')
                    break
                uvs.append(uv_index)
                print("UV Index:", uv_index)
                x += 1
                time.sleep(0.2)
    except Exception as e:
        print(e)
    finally:
        p.disconnect()
        print('closing up')


peripheral('Sunlight')
