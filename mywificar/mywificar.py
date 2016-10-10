import MotorBridge
import time

MotorLeft        = 1
MotorRight       = 4
ClockWise        = 1
CounterClockWise = 2
PwmDuty          = 90
Frequency        = 1000


motor = MotorBridge.MotorBridgeCape()
motor.DCMotorInit(MotorLeft,Frequency)
motor.DCMotorInit(MotorRight,Frequency)


def goFront():
    motor.DCMotorMove(MotorRight,ClockWise,PwmDuty)
    motor.DCMotorMove(MotorLeft,CounterClockWise,PwmDuty)

def goBack():
    motor.DCMotorMove(MotorLeft,ClockWise,PwmDuty)
    motor.DCMotorMove(MotorRight,CounterClockWise,PwmDuty)

def turnLeft():
    return 0
def turnRight():
    return 0
def stop():
    motor.DCMotorStop(MotorLeft)
    motor.DCMotorStop(MotorRight)

if __name__ == '__main__':
    goFront()
    time.sleep(2)
    goBack()
    time.sleep(2)
    stop()
    time.sleep(1) 
