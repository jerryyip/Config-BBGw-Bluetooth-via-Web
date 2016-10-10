import MotorBridge
import time
 
MotorName        = 4
ClockWise        = 1
CounterClockWise = 2
PwmDuty          = 90
Frequency        = 1000
 
if __name__=="__main__":
    motor = MotorBridge.MotorBridgeCape()
    motor.DCMotorInit(MotorName,Frequency)
    while True:
        motor.DCMotorMove(MotorName,ClockWise,PwmDuty)
        time.sleep(2)
        motor.DCMotorMove(MotorName,CounterClockWise,PwmDuty)
        time.sleep(2)
        print "hello"
        motor.DCMotorStop(MotorName)
        time.sleep(2)
