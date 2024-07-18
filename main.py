from pyscript import document, window, when
import andrea_terminal
import restapi
import file_transfer
import file_os
import json

##############################################
# Terminal Code                              #
##############################################

ARDUINO_NANO = 128
SPIKE = 256
path = "https://raw.githubusercontent.com/chrisbuerginrogers/SPIKE_Prime/main/BLE/BLE_CEEO.py"


async def on_connect(event):
    if terminal.connected:
        connect.innerText = 'connect up'
        await terminal.board.disconnect()
    else:
        await terminal.board.connect('repl')
        if terminal.connected:
            connect.innerText = 'disconnect'
            await file_os.getList(terminal, list)
            await terminal.eval('\x03', True)
    for b in btns:
        b.disabled = not terminal.connected


def on_disconnect():
    connect.innerText = 'connect up'
    python.code = ''
    list.options.length = 0
    terminal.update(0)


async def on_load(event):
    if terminal.connected:
        name = path.split('/')[-1]
        print('path, name: ', path, name)
        reply = await restapi.get(path)
        status = await terminal.download(name, reply)
        if not status:
            window.alert(f"Failed to load {name}")
    else:
        window.alert('connect to a processor first')


def handle_board(event):
    code = event.code
    if terminal.connected:
        await terminal.eval('\x05'+code+'\x04')
        terminal.focus()
        return False  # return False to avoid executing on browser
    else:
        return True


def on_select(event):
    python.code = await file_os.read_code(terminal, list)


def on_clear(event):
    python.code = ''


@when("click", "#test")
def on_test(event):
    python.code = test_code


@when("click", "#data")
def on_data(event):
    data = terminal.buffer


connect = document.getElementById('connect')
library = document.getElementById('library')
progress_bar = document.getElementById('progress')
list = document.getElementById('files')
python = document.getElementById('mpCode')
remote = document.getElementById('upload')
clear = document.getElementById('clear')

connect.onclick = on_connect
library.onclick = on_load
# list.onchange = on_select
remote.onclick = on_select
clear.onclick = on_clear
python.handleEvent = handle_board

terminal = andrea_terminal.Terminal()
# terminal = file_transfer.Ampy(ARDUINO_NANO, progress_bar)
terminal.disconnect_callback = on_disconnect

btns = [library, remote, clear]
for b in btns:
    b.disabled = not terminal.connected

##############################################
# Connect up to the PicoW and get Data       #
##############################################
