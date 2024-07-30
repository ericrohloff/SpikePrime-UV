from bluetooth import Listen

# Create and setup Central
central = Listen('PeripheralDevice', verbose=True)
try:
    if central.connect_up():
        print('Central connected to peripheral device')
        # Wait for data and print it
        while central.is_connected:
            time.sleep(2)  # Wait for data to be received
            if central.is_any:
                received_data = central.read()
                print('Received:', received_data)
                # Optionally, send a reply
                reply = 'Reply from Central'
                central.send(reply)
                print('Reply sent:', reply)
    else:
        print('Failed to connect')
except Exception as e:
    print('Error:', e)
finally:
    # Clean up
    central.disconnect()
    print('Closing central mode')
