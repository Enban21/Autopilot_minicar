import RPi.GPIO as GPIO
import time

servo_pin = 21  # サーボモータの接続ピン

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)  # 50HzのPWM信号
pwm.start(7.5)  # 中立位置

def set_servo_angle(angle):
    duty = 2.5 + (angle / 18.0)
    pwm.ChangeDutyCycle(duty)

try:
    while True:
        # ファイルからステアリング角度を読み取る
        with open("steering_angle.txt", "r") as file:
            steering_angle = float(file.read())

        set_servo_angle(steering_angle)
        print(steering_angle)
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

pwm.stop()
GPIO.cleanup()
