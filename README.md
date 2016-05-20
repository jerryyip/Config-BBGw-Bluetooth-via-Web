# Config-BBGw-Bluetooth-via-Web
We usually use the bash command line to configure the BBGw Bluetooth, so that it can be connected to other Bluetooth devices (if you do not know how to use the bash command line configuration, click here to view the tutorial). But today, we will try to use the python-flask framework on the BBGw to build a small server, and to generate a page to configure the Bluetooth. Hope you can get inspiration from this simple tutorial, we look forward to your excellent works！

This tutorial is based on Python 2.7.

1.Please connect your BBGw to wifi first , and switch to the root account.

2.Install virtualenv(If it fail to install,please ‘apt-get update’ first and retry.)
apt-get install python-virtualenv

3.Create your environment under absolute path directory /home/debian/bin 
  $ cd /home/debian/bin 
  $ mkdir myproject
  $ cd myproject
  $ mkdir templates
  $ virtualenv venv

4.Active your ‘venv’ environment ,and install the following python package
 $  . venv/bin/activate 
 $ pip install Flask
 $ pip install pexpect
 $ pip install flask-socketio

5.Copy app.py and bluetoothtest.py to absolute path directory /home/debian/bin/myproject (from your u disk or nfs server),and copy index.html to absolute path directory /home/debian/bin/myproject/templates 
 Mount your u disk or nfs server which contains the following file 
 $ cp app.py /home/debian/bin/myproject
 $ cp bluetoothtest.py /home/debian/bin/myproject
 $ cp index.html /home/debian/bin/myproject/templates

6.Go
$ python app.py

7.Visit 192.168.x.x:5000(192.168.x.x means your BBGw’s IP,you can view it with  bash command ‘ifconfig’.Also you computer needs to be in this local area network )
Like this:
192.168.199.200 is my BBGw’s IP address of wifi network.(not 192.168.7.2&192.168.8.1)

8.Enter your device’s bluetooth mac address(such as your bluetooth earphone) ,click ‘pair’.Wait about 10 seconds.

Then you will receive the result.
