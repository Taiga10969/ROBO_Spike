from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

hub = PrimeHub()

#hub.light_matrix.show_image('HAPPY')


def init():
    color_sensor = ColorSensor('A')
    motor_pair = MotorPair('E','F')
    return color_sensor, motor_pair

def move(color_sensor, motor_pair):
    motor_pair.set_default_speed(speed=20)
    # ライントレースinit
    target = (48+97) / 2
    P_gain =6

    #start to color area
    motor_pair.move(amount=3.5,unit='rotations',steering=0) #直進
    motor_pair.move(amount=0.5,unit='rotations',steering=100) #右回転
    motor_pair.move(amount=1.8,unit='rotations',steering=0) #直進
    motor_pair.move(amount=0.5,unit='rotations',steering=100) #右回転
    motor_pair.move(amount=3.5,unit='rotations',steering=0) #直進
    motor_pair.move(amount=0.5,unit='rotations',steering=-100) #左回転
    motor_pair.move(amount=1.5,unit='rotations',steering=0) #直進
    motor_pair.move(amount=0.5,unit='rotations',steering=-100) #左回転
    motor_pair.move(amount=1.8,unit='rotations',steering=0) #直進
    motor_pair.move(amount=0.5,unit='rotations',steering=100) #右回転

    motor_pair.start()
    while True:
        if color_sensor.get_color()=='red' or color_sensor.get_color()=='blue':
            break
    motor_pair.stop()


    # ライントレース
    # clor_area=赤色の場合
    if color_sensor.get_color()=='red':
        motor_pair.move(amount=0.5,unit='rotations',steering=-100) #左回転
        motor_pair.move(amount=1.2,unit='rotations',steering=0) #直進
        #カラーセンサーが赤を読むまで繰り返す
        while color_sensor.get_color() != 'red':
            #現在の反射光の値を代入
            reflected_light = color_sensor.get_reflected_light()
            #【反射光の値 - 白と黒の中間値 × Pゲイン】の値の向きに走行
            motor_pair.start(int((reflected_light - target) * P_gain))
        motor_pair.stop() #停止
        motor_pair.move(amount=1.5,unit='rotations',steering=0) #直進


    # clor_area=青色の場合
    if color_sensor.get_color()=='blue':
        motor_pair.move(amount=0.5,unit='rotations',steering=100) #右回転
        motor_pair.move(amount=1.0,unit='rotations',steering=0) #直進
        #カラーセンサーが赤を読むまで繰り返す
        while color_sensor.get_color() != 'blue':
            #現在の反射光の値を代入
            reflected_light = color_sensor.get_reflected_light()
            #【反射光の値 - 白と黒の中間値 × Pゲイン】の値の向きに走行
            motor_pair.start(int(-(reflected_light - target) * P_gain))
        motor_pair.stop()#停止
        motor_pair.move(amount=1.5,unit='rotations',steering=0) #直進


# if __name__=='__main__':
color_sensor, motor_pair = init()
move(color_sensor, motor_pair)
