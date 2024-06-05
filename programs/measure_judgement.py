from measure_distance import distance
import RPi.GPIO as GPIO 
import time

# GPIOピンの設定
IN1_PIN = 27  # Raspberry PiのGPIOピン番号
IN2_PIN = 17

def setup():
    GPIO.setmode(GPIO.BCM)  # BCMピン番号を使用
    GPIO.setup(IN1_PIN, GPIO.OUT)
    GPIO.setup(IN2_PIN, GPIO.OUT)

def forward():
    GPIO.output(IN1_PIN, GPIO.HIGH)
    GPIO.output(IN2_PIN, GPIO.LOW)

def backward():
    GPIO.output(IN1_PIN, GPIO.LOW)
    GPIO.output(IN2_PIN, GPIO.HIGH)

def stop():
    GPIO.output(IN1_PIN, GPIO.LOW)
    GPIO.output(IN2_PIN, GPIO.LOW)

def cleanup():
    GPIO.cleanup()

setup()

try:
    while True:
        if distance > 35:
            print("モーター前進")
            forward()
            time.sleep(5)
            print("モーター後退")
            backward()
            time.sleep(5)
            print("モーター停止")
            stop()
            time.sleep(5)
        else:
            stop()
            print("停止")
            
except KeyboardInterrupt:
  GPIO.cleanup() 