import RPi.GPIO as GPIO # RPi.GPIOモジュールをGPIOとして使用
import time             # timeモジュールの読み込み

gpio_trig = 22    # トリガーピンのGPIO番号を定義
gpio_echo = 23    # エコーピンのGPIO番号を定義

GPIO.setmode(GPIO.BCM)          # GPIO番号で指定する設定
GPIO.setup(gpio_trig, GPIO.OUT) # トリガーピンを出力に設定
GPIO.setup(gpio_echo, GPIO.IN)  # エコーピンを入力に設定

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