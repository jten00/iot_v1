from time import sleep
import machine
import network
import urequests as requests

DELAY = 10
SSID = "Wokwi-GUEST"
PASSWORD = ""
WLAN = network.WLAN(network.STA_IF)

pir = machine.Pin(27, machine.Pin.IN)
count = 0

def connectWIFI():
    WLAN.active(True)
    WLAN.connect(SSID, PASSWORD)
    while not WLAN.isconnected():
        print(".", end="")
        sleep(0.1)
    print("Connected")
    print(WLAN.ifconfig())
    return None

def sendData(value):
    try:
        DATA_ENDPOINT = "http://20.238.121.237:80/api/update"
        response = requests.get(f"{DATA_ENDPOINT}?value={value}")
        print("Response status code:", response.status_code)
    except Exception as error:
        print("Request failed:", error)
    return None

def on_pir_triggered(pin):
    global count
    if pin.value() == 1:
        count += 1
        print("\nDoor opened")
        print("Times door has been opened:{}".format(count),end="")
    return None

def operate():
    pir.irq(trigger=machine.Pin.IRQ_RISING, handler=on_pir_triggered)
    while True:
        value = count
        sendData(value)
        sleep(DELAY)
    return None

def main():
    connectWIFI()
    print("System startup.")
    operate()
    return None

main()