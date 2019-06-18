 # XinaBox CW01 + BM11 + Micro:Bit
from micropython import mem_info
from microbit import *
from utime import sleep,sleep_ms

def CW01AT(t,raw=False,wait=None,useUART=1):
    if useUART == 1 or useUART == 2:
        uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=pin1, rx=pin0)
    sleep_ms(10)
    if raw:
        uart.write(bytearray(t))
        return
    else:
        uart.write((t+"\r\n"))
    sleep_ms(10)
    j = 0
    while not uart.any():
        j= j+1
        if j>10:
            break
        sleep_ms(10)
    data = uart.readline()
    i = 0
    rc = -1
    tall = []
    while(i<100): # 10 seconds max
        i=i+1
        sleep_ms(50)
        if wait and data==bytearray(wait+"\r\n"):
            rc = 1
        if data == b'OK\r\n':
            rc = 1
        if data == b'ERROR\r\n':
            rc = 0
        if rc>-1:
            break
        if data and len(data)>2 and str(data, "utf-8")[:2] != "AT":
            data = str(data[:-2], "utf-8")
            tall.append(data)
        j = 0
        while not uart.any():
            j= j+1
            if j>10:
                break
            sleep_ms(10)
        data = uart.readline()
    if useUART == 1 or useUART == 3:
        uart.init(115200)
        if rc==1:
            pass
        elif rc==0:
            print(t + ": ERROR")
        else:
            print(t +": ??????")
        if tall:
            print(', '.join(tall))


CW01AT("AT+TEST")
sleep(0.1)

# Fill in below
_WIFI_SSID = "<ssid>"
_WIFI_PASSWORD = "<password>"
_SERVER = "<proxy>"
_PORT = 80
_TIME_ZONE = <timezone>
mem_info()

def main():
    CW01AT("AT") # Clear the channel
    sleep(5)
    EspConnect(_SERVER,_PORT)
    sleep(2)
    print(i2c.scan())


def EspConnect(url, port):
    # RED LED on CW01 and SQUARE on Micro:Bit
    display.show(Image.SQUARE)
    # Connect to WiFI
    CW01AT("AT+CWMODE=3")
    sleep(0.1)
    CW01AT("AT+CWJAP=\""+_WIFI_SSID+"\",\""+_WIFI_PASSWORD+"\"")
    sleep(0.1)
    # CW01AT("AT+CIFSR","+CIFSR")
    display.show(Image.CHESSBOARD)

    btn = 0

    while True:
        #Connect to Server

        CW01AT("AT+CIPSTART=\"TCP\",\""+url+"\","+str(port))

        sleep(0.2)

        temp = str(temperature())

        if(button_b.is_pressed()):
            btn=1
        else:
            btn=0

        payload="{\"temperature\":"+temp+"}"
        req =("POST <url> HTTP/1.1\r\n"+
            "Host:<proxy>\r\n"+
            "Content-Length:%d\r\n"%len(payload)+
            "Content-Type:application/json\r\n\r\n"+
            payload+"\r\n")


        CW01AT("AT+CIPSEND=%d"%len(req),useUART=2)
        sleep(0.5)
        CW01AT(req,True,useUART=0)
        sleep(1)

    CW01AT("AT+CIPCLOSE",useUART=0)
    sleep(10)
    CW01AT("AT",useUART=3)
    display.show(Image.DIAMOND)


if __name__ == '__main__':
    main()
    #print("Finished!")
