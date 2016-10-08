import time
import mraa

x = mraa.Pwm(62)
x.period_us(700)
x.enable(True)
value = 0

def myled(times=1,delays=0.01):
    value = 0
    if (times <= 0):
        print("times must be more than 0")
        return 0
    for mytime in range(times):
        for i in range(200):
    	    if (value < 1):
        	x.write(value)
    	    if ((value >= 1) and (value < 2)):
        	x.write(2-value)
    	    value = value + 0.01
    	    time.sleep(delays)
    	    if (value >= 2.0):
        	value = 0
def myledon():
    x.write(0)

def myledoff():
    x.write(1)
        
if __name__ == '__main__':
    print("defulat")
    myled()
    print("times = 4,delays = 0.02")
    myled(4,0.02)
