import time
import pexpect
import subprocess
import sys
import os
import syslog

def bluetooth_preInit():
    status = 'error'
    print "bluetooth_preInit!"
    # Initialize bluetooth device

    child = pexpect.spawn("bb-wl18xx-bluetooth")
    out = child.expect(["Device setup complete", "Can't initialize device: Success", "Initialization timed out",  pexpect.EOF])
    print "bb-wl18xx-bluetooth result: ", out
    if 2 > out:
	return 'ok'
    if 2 == out:
        child = pexpect.spawn("bb-wl18xx-bluetooth")
        out = child.expect(["Device setup complete", "Can't initialize device: Success", "Initialization timed out", pexpect.EOF])
        print "bb-wl18xx-bluetooth result: ", out
        if 1 < out:
            return status
    # Remove all bluetooth mac adress info        
   # os.system("rm /var/lib/bluetooth/* -rf")
    # Restart bluetooth service
   #os.system("systemctl restart bluetooth")
   # subprocess.call(['systemctl', 'restart', 'bluetooth'])
    #time.sleep(5)       
   # results = os.popen("ls /var/lib/bluetooth/").read()
   # print "len(results): ", len(results)
   # if 18 == len(results):
	status = 'ok'
    return status

class BluetoothctlError(Exception):
    """This exception is raised, when bluetoothctl fails to start."""
    pass


class Bluetoothctl:
    """A wrapper for bluetoothctl utility."""

    def __init__(self):                        
        f = file("./plog.out", 'w')
        # Start to open bluetoothctl
        out = subprocess.check_output("rfkill unblock bluetooth", shell = True)
        self.child = pexpect.spawn("bluetoothctl")
        
        # TO-DO
        # If run bluetoothctl and can't get beaglebone MAC address, then reinitialize again
        
        self.child.logfile = f                                                   
            
    def __del__(self):
        self.child.sendline("quit")
        # print self.child.before
        self.child
        print "del function"
        
    def get_output(self, command, pause = 0):
        """Run a command in bluetoothctl prompt, return output as a list of lines."""
        self.child.send(command + "\n")
        time.sleep(pause)
        start_failed = self.child.expect(["bluetooth", pexpect.EOF])

        if start_failed:
            raise BluetoothctlError("Bluetoothctl failed after running " + command)

        return self.child.before.split("\r\n")

    def start_scan(self):        
        """Start bluetooth scanning process."""
        try:
            out = self.get_output("scan on")
        except BluetoothctlError, e:
            print(e)
            return None

    def make_discoverable(self):
        """Make device discoverable."""
        try:
            out = self.get_output("discoverable on")
        except BluetoothctlError, e:
            print(e)
            return None

    def parse_device_info(self, info_string):
        """Parse a string corresponding to a device."""
        device = {}
        block_list = ["[\x1b[0;", "removed"]
        string_valid = not any(keyword in info_string for keyword in block_list)

        if string_valid:
            try:
                device_position = info_string.index("Device")
            except ValueError:
                pass
            else:
                if device_position > -1:
                    attribute_list = info_string[device_position:].split(" ", 2)
                    device = {
                        "mac_address": attribute_list[1],
                        "name": attribute_list[2]
                    }

        return device

    def get_available_devices(self):
        """Return a list of tuples of paired and discoverable devices."""
        try:
            out = self.get_output("devices")
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            available_devices = []
            for line in out:
                device = self.parse_device_info(line)
                if device:
                    available_devices.append(device)

            return available_devices

    def get_paired_devices(self):
        """Return a list of tuples of paired devices."""
        try:
            out = self.get_output("paired-devices")
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            paired_devices = []
            for line in out:
                device = self.parse_device_info(line)
                if device:
                    paired_devices.append(device)

            return paired_devices

    def get_discoverable_devices(self):
        """Filter paired devices out of available."""
        available = self.get_available_devices()
        paired = self.get_paired_devices()

        return [d for d in available if d not in paired]

    def get_device_info(self, mac_address):
        """Get device info by mac address."""
        try:
            out = self.get_output("info " + mac_address)
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            return out

    def pair(self, mac_address):
        """Try to pair with a device by mac address."""
        try:
            out = self.get_output("pair " + mac_address, 4)
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            res = self.child.expect(["Failed to pair", "Pairing successful", pexpect.EOF])
            success = True if res == 1 else False
            return success

    def remove(self, mac_address):
        """Remove paired device by mac address, return success of the operation."""
        try:
            out = self.get_output("remove " + mac_address, 3)
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            res = self.child.expect(["not available", "Device has been removed", pexpect.EOF])
            success = True if res == 1 else False
            return success

    def connect(self, mac_address):
        """Try to connect to a device by mac address."""
        try:
            out = self.get_output("connect " + mac_address, 2)
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            res = self.child.expect(["Failed to connect", "Connection successful", pexpect.EOF])
            success = True if res == 1 else False
            return success

    def disconnect(self, mac_address):
        """Try to disconnect to a device by mac address."""
        try:
            out = self.get_output("disconnect " + mac_address, 2)
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            res = self.child.expect(["Failed to disconnect", "Successful disconnected", pexpect.EOF])
            success = True if res == 1 else False
            return success

#    def run_test(self,dist_mac_addr = "78:09:73:C8:77:50"):
#    def run_test(self,dist_mac_addr = "51:91:E2:BF:AE:47"):
#    def run_test(self,dist_mac_addr = "74:51:BA:F2:E4:72"):
    def run_test(self,dist_mac_addr):
        status = 'error'
		print dist_mac_addr        
        #timestart = time.time()
		self.child.sendline("devices")
		print "devices"
		results = self.child.expect([dist_mac_addr, pexpect.EOF, pexpect.TIMEOUT])
		#if the mac_addr dont exist,then scan on 
		if results != 0
			self.child.sendline("scan on")
			print "Scan on!"
#        	time.sleep(10)
			results = self.child.expect([dist_mac_addr, "Failed to start", pexpect.EOF, pexpect.TIMEOUT], timeout=60)
			if 3 == results:
				print "scan timeout"
				self.child.sendline("scan off")
				return status
			if results > 0:
				print "scan on result: ", results
				return status
 		#if the mac_addr exist in devices list or in the scan list,then pair      
        if 0 == results :
            # pair device for three times 
            self.child.sendline("pair " + dist_mac_addr)
            results = self.child.expect(["Paired: yes", "Fail", pexpect.EOF])
            if 0 != results:
                self.child.sendline("pair " + dist_mac_addr)
                results = self.child.expect(["Paired: yes", "Fail", pexpect.EOF])
                if 0 != results:
                    self.child.sendline("pair " + dist_mac_addr)
                    results = self.child.expect(["Paired: yes", "Fail", pexpect.EOF])
                    if 0!= results:
                        return status
            if 0 == results:
                # connect device for three time
                print "Pair ok!"
                self.child.sendline("connect " + dist_mac_addr)
                results = self.child.expect(["Connection successful", "Fail", "org.bluez.Error.Failed", pexpect.EOF])
                if 0 < results:
		    time.sleep(2)
                    self.child.sendline("connect " + dist_mac_addr)
                    results = self.child.expect(["Connection successful", "Fail", "org.bluez.Error.Failed", pexpect.EOF])
                    if 0 < results:
#                        self.child.sendline("connect " + dist_mac_addr)
#                        results = self.child.expect(["Connection successful", "Fail", "org.bluez.Error.Failed", pexpect.EOF])
#                        if 0 < results:
                            return status
                time.sleep(1)
                if 0 == results:
#                    print("connect: " + dist_mac_addr)
#                    if dist_mac_addr=="51:91:E2:BF:AE:47" :     
#                        print "unit1 play music"
#                        os.system("mpg123 /root/factory_test/music/unit1.mp3")
#                    elif dist_mac_addr=="49:7A:10:6F:2D:D4":
#                        print "unit2 play music"
#                        os.system("mpg123 /root/factory_test/music/unit2.mp3")
#                    elif dist_mac_addr=="EF:50:7B:BD:C8:16":  
#                        print "unit3 play music"  
#                        os.system("mpg123 /root/factory_test/music/unit3.mp3")
#                    elif dist_mac_addr=="3A:6B:13:A0:32:B6":
#                        print "unit4 play music"
#                        os.system("mpg123 /root/factory_test/music/unit4.mp3")
#                    elif dist_mac_addr=="78:09:73:C8:77:50":
#                       print "unit5 play music"     
#                        os.system("mpg123 /root/factory_test/music/unit5.mp3")
#                    elif dist_mac_addr=="FC:CD:B3:39:96:66":
#                        print "unit6 play music"
#                        os.system("mpg123 /root/factory_test/music/unit6.mp3")                 
#                    time.sleep(2)
                    # Disconnect bluetooth
#                    self.child.sendline("disconnect " + dist_mac_addr)
                    status = 'ok'
                    time.sleep(2)                    
       # self.child.sendline("quit")
        return status

if __name__ == "__main__":
    if 'ok' == bluetooth_preInit():
		dist_mac_addr=sys.stdin.readline()
        print dist_mac_addr
		bl = Bluetoothctl()
        result = bl.run_test(dist_mac_addr)
        print "bluetooth test result: ", result
    else:
        print "error" 
