# Run this code on the SPIKE Prime to listen for UV index data
from BLE_CEEO import Listen
import time


def central(name):
    uv_indices = []
    try:
        L = Listen(name, verbose=True)
        if L.connect_up():
            # print('L connected')
            while L.is_connected:
                time.sleep(4)
                if L.is_any:
                    reply = L.read().strip()  # Strip leading/trailing whitespace
                    # print(f"Received: {reply}")
                    # Split the received data by newline characters
                    replies = reply.split('\n')
                    for r in replies:
                        if r:  # Ensure the string is not empty
                            try:
                                uv_index = float(r)
                                # Append the received UV index to the list
                                uv_indices.append(uv_index)
                            except ValueError:
                                # print(f"Invalid syntax for number: {r}")
                                # Send a portion of the reply back, if needed
                                L.send(reply[:20])
    except Exception as e:
        print(e)
    finally:
        L.disconnect()
        print("UV Indices:", uv_indices)  # Print the list of UV indices


central('Sunlight')
