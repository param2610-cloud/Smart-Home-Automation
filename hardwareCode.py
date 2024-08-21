import machine
import network
import urequests  
import time


THINGSPEAK_API_KEY = 'GV9045VTF0P3JNQV'
THINGSPEAK_CHANNEL_ID = '2632362'


WIFI_SSID = 'your-ssid'
WIFI_PASSWORD = 'your-password'


pir_sensor = machine.Pin(16, machine.Pin.IN)  
servo_pin = machine.Pin(15)  
servo = machine.PWM(servo_pin, freq=50)  


def set_servo_angle(angle):
    
    duty = int((angle / 180) * 1000 + 1000)  
    servo.duty_u16(duty * 65535 // 20000)  


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        time.sleep(1)
    print('Connected to Wi-Fi:', WIFI_SSID)
    print('IP Address:', wlan.ifconfig()[0])


def send_motion_to_thingspeak(motion_detected):
    url = f'https://api.thingspeak.com/update?api_key={THINGSPEAK_API_KEY}'
    url2 = 'https://smart-home-automation.onrender.com/motion-detected'
    data = {
        'field1': 1 if motion_detected else 0  
    }
    response = urequests.get(url, params=data)
    response2 = urequests.post(url2)
    print('Data sent to ThingSpeak:', response.text)
    print('Email sent ', response2.text)


def main():
    connect_wifi()

    while True:
        if pir_sensor.value() == 1:  
            print('Motion detected!')
            send_motion_to_thingspeak(True)

            
            time.sleep(5)  
            
            door_open = check_door_status()  
            if door_open:
                print('Opening door...')
                set_servo_angle(90)  
            else:
                print('Closing door...')
                set_servo_angle(0)  

        else:
            print('No motion detected')
            send_motion_to_thingspeak(False)

        time.sleep(1)  


def check_door_status():
    url = f'https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/fields/2.json?api_key={THINGSPEAK_API_KEY}&results=1'
    response = urequests.get(url)
    data = response.json()
    door_status = int(data['feeds'][0]['field2'])  
    return door_status == 1  


main()
