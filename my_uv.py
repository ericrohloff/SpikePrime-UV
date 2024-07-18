from machine import ADC, Pin

adc = ADC(Pin(27))  # Initialize ADC on GPIO pin 27
value = adc.read_u16()


def get_voltage(value):
    ref = 3.3
    voltage = (value / 65535) * ref
    return voltage


def get_illumination(value):
    return value * 307


def get_uvindex(value):
    ref = 3.3
    voltage = (value / 65535) * ref
    ill = voltage * 307
    uv = ill/35
    return uv


v = get_voltage(value)
i = get_illumination(v)


print(v)
print(i/35)
