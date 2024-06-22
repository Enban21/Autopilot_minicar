import cv2
import numpy as np
import subprocess

def detect_lane_lines(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    return edges

def find_lanes(edges):
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=100, maxLineGap=50)
    left_lane = []
    right_lane = []
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                slope = (y2 - y1) / (x2 - x1)
                if slope < 0:
                    left_lane.append(line)
                else:
                    right_lane.append(line)
    return left_lane, right_lane

def average_lane_position(lane_lines):
    x_coords = []
    y_coords = []
    for line in lane_lines:
        for x1, y1, x2, y2 in line:
            x_coords.extend([x1, x2])
            y_coords.extend([y1, y2])
    if x_coords and y_coords:
        poly_fit = np.polyfit(y_coords, x_coords, 2)  # 2次多項式でフィッティング
        return poly_fit
    return None

def calculate_curvature(poly_fit, y_eval, pixel_to_meter_ratio):
    if poly_fit is not None:
        A = poly_fit[0] * pixel_to_meter_ratio  # 係数をメートル単位に変換
        B = poly_fit[1] * pixel_to_meter_ratio
        curvature = ((1 + (2 * A * y_eval * pixel_to_meter_ratio + B) ** 2) ** 1.5) / np.abs(2 * A)
        return curvature
    return float('inf')

def calculate_steering_angle(left_fit, right_fit, frame_height, pixel_to_meter_ratio):
    if left_fit is not None and right_fit is not None:
        left_bottom = np.polyval(left_fit, frame_height)
        right_bottom = np.polyval(right_fit, frame_height)
        lane_center = (left_bottom + right_bottom) / 2
        frame_center = frame.shape[1] / 2
        offset = lane_center - frame_center
        steering_angle = -offset / frame.shape[1] * 180  # ステアリング角度を計算
        return steering_angle
    return 0

def steering_angle_to_servo_angle(steering_angle):
    # ステアリング角度をサーボ角度に変換
    servo_angle = 90 + steering_angle
    servo_angle = max(0, min(servo_angle, 180))  # サーボ角度を0度から180度に制限
    return servo_angle

# カメラ設定
width = 640
height = 480
fps = 30

# libcamera-vidコマンドでカメラ映像を取得
process = subprocess.Popen([
    "libcamera-vid",
    "--width", str(width),
    "--height", str(height),
    "--framerate", str(fps),
    "-o", "-", "--codec", "mjpeg",
    "--timeout", "0"
], stdout=subprocess.PIPE, bufsize=10)

pixel_to_meter_ratio = 0.01  # 1ピクセル = 0.01メートル（仮定）

try:
    while True:
        # カメラ映像を取得してOpenCVで処理
        byte_chunk = process.stdout.read(width * height * 3)
        if len(byte_chunk) != width * height * 3:
            break
        frame = np.frombuffer(byte_chunk, dtype=np.uint8).reshape((height, width, 3))

        edges = detect_lane_lines(frame)
        left_lane, right_lane = find_lanes(edges)

        left_fit = average_lane_position(left_lane)
        right_fit = average_lane_position(right_lane)

        steering_angle = calculate_steering_angle(left_fit, right_fit, frame.shape[0], pixel_to_meter_ratio)

        # 曲率を計算
        left_curvature = calculate_curvature(left_fit, frame.shape[0] // 2, pixel_to_meter_ratio)
        right_curvature = calculate_curvature(right_fit, frame.shape[0] // 2, pixel_to_meter_ratio)

        print(f"Left curvature: {left_curvature:.2f} m⁻¹, Right curvature: {right_curvature:.2f} m⁻¹")

        # ステアリング角度をファイルに書き込む
        servo_angle = steering_angle_to_servo_angle(steering_angle)
        with open("steering_angle.txt", "w") as file:
            file.write(str(servo_angle))

        print(f"Servo angle: {servo_angle:.2f} degrees")

        if left_fit is not None:
            cv2.line(frame, (int(np.polyval(left_fit, frame.shape[0])), frame.shape[0]), (int(np.polyval(left_fit, 0)), 0), (255, 0, 0), 2)
        if right_fit is not None:
            cv2.line(frame, (int(np.polyval(right_fit, frame.shape[0])), frame.shape[0]), (int(np.polyval(right_fit, 0)), 0), (255, 0, 0), 2)

        cv2.imshow('Frame', frame)
        cv2.imshow('Edges', edges)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass

process.terminate()
cv2.destroyAllWindows()
