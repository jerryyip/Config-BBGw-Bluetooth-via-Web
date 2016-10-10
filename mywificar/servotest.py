import MotorBridge
import time
ServoName   =  3
Frequency   =  50
Angle1      =  20
Angle2      =  160
 
if __name__=="__main__":
    motor = MotorBridge.MotorBridgeCape()
    motor.ServoInit(ServoName,Frequency)
 
    while True:
        print 'Servo Test'
        motor.ServoMoveAngle(ServoName,Angle1)
        time.sleep(2)
        motor.ServoMoveAngle(ServoName,Angle2)
        time.sleep(2)
