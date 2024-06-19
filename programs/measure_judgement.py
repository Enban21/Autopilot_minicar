import RPi.GPIO as GPIO 
import time

# GPIOピンの設定
IN1_PIN = 27  # Raspberry PiのGPIOピン番号
IN2_PIN = 17
gpio_trig = 22    # トリガーピンのGPIO番号を定義
gpio_echo = 23    # エコーピンのGPIO番号を定義
gpio_trig = 22    # トリガーピンのGPIO番号を定義
gpio_echo = 23    # エコーピンのGPIO番号を定義


GPIO.setmode(GPIO.BCM)  # BCMピン番号を使用
GPIO.setup(IN1_PIN, GPIO.OUT)
GPIO.setup(IN2_PIN, GPIO.OUT)
GPIO.setup(gpio_trig, GPIO.OUT) # トリガーピンを出力に設定
GPIO.setup(gpio_echo, GPIO.IN)  # エコーピンを入力に設定

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



try:
  while True:
    # トリガー信号の生成
    GPIO.output(gpio_trig, GPIO.HIGH) # トリガーピン出力をHIGHにして
    time.sleep(0.00001)               # 10マイクロ秒保持し、
    GPIO.output(gpio_trig, GPIO.LOW)  # その後LOWにする
    # エコー信号が0から1になる時刻を記録
    while GPIO.input(gpio_echo) == 0: # エコー信号がLOWの間
      EndTimeLow = time.time()        # 現在時刻をEndTimeLowに代入
    # エコー信号が1から0になる時刻を記録
    while GPIO.input(gpio_echo) == 1: # エコー信号がHIgHの間
      EndTimeHigh = time.time()       # 現在時刻をEndTimeHighに代入

    duration = EndTimeHigh - EndTimeLow # エコーがHIGHの期間を算出
    distance = duration * 17000         # 距離の計算

    print("Distance = ", format(distance, '.2f'), "cm") # 計算結果をコンソールに出力
    time.sleep(0.1)
except KeyboardInterrupt:
  GPIO.cleanup() 



#距離に応じて動作判断
try:
    while True:
        if distance > 10:
            print("モーター前進")
            forward()
        else:
            stop()
            print("停止")
            
except KeyboardInterrupt:
  GPIO.cleanup() 