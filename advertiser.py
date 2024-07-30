# main_peripheral.py
from bluetooth import Yell
import time

# Create and setup Peripheral
peripheral = Yell('PeripheralDevice', verbose=True)
try:
    print('Starting peripheral...')
    while True:
        # Continuously send data and print any received data
        if peripheral.is_connected:
            data_to_send = 'Hello from Peripheral!'
            peripheral.send(data_to_send)
            print('Data sent:', data_to_send)
            time.sleep(2)  # Wait before sending the next message
            # Optionally, read any incoming data
            if peripheral.is_any:
                print('Received:', peripheral.read())
        else:
            print('Peripheral is not connected. Advertising...')
            peripheral._advertise()
            time.sleep(5)  # Wait before checking the connection again
except Exception as e:
    print('Error:', e)
finally:
    # Clean up
    peripheral.disconnect()
    print('Closing peripheral mode')
