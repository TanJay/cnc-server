# from serial import Serial
# import time
# ser = Serial('/dev/cu.usbmodem1421')  # open first serial port
# time.sleep(5)
# print ser.portstr       # check which port was really used
# ser.write("G01 Z+10")      # write a string
# ser.close()
import time
import serial
import paho.mqtt.client as mqtt


# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/cu.usbmodem1421',
    baudrate=9600
)

ser.isOpen()

print 'Enter your commands below.\r\nInsert "exit" to leave the application.'

out = ''
time.sleep(4)
while ser.inWaiting() > 0:
    out += ser.read(1)
print out
ser.write("G01 Z-1" + '\n')
input=1
# while 1 :
#     # get keyboard input
#     input = raw_input(">> ")
#     print input
#     # Python 3 users
#     # input = input(">> ")
#     if input == 'exit':
#         ser.close()
#         exit()
#     else:
#         # send the character to the device
#         # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
#         ser.write(input + '\n')
#         out = ''
#         # let's wait one second before reading output (let's give device time to answer)
#         time.sleep(1)
#         while ser.inWaiting() > 0:
#             out += ser.read(1)
#
#         if out != '':
#             print ">>" + out

############
def on_message(client, userdata, message):
    value = "G01 Z" + str(message.payload) + '\r\n'
    ser.write(str(value).encode())
    print str(message.payload.decode("utf-8"))
    # print("message received " ,str(message.payload.decode("utf-8")))
    # print("message topic=",message.topic)
    # print("message qos=",message.qos)
    # print("message retain flag=",message.retain)
########################################
broker_address="34.213.68.150"
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
print("Subscribing to topic","cnc/z")
client.subscribe("/cnc/z")
# client.on_message=on_message #attach function to callback
# print("Publishing message to topic","cnc/z")
# client.publish("cnc/z","OFF")
time.sleep(1000) # wait
# client.loop_stop() #stop the loop