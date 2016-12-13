'''
/*
 * Modified down
 *
 * Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import getopt

# Command Line Parameters
host = "YOUR REST API EndPoint URL goes here"
rootCAPath = "root-CA.crt"
certificatePath = "Multipass.cert.pem"
privateKeyPath = "Multipass.private.key"
topiccmdPath = "$aws/things/Multipass/shadow/command"
topicstatusPath = "$aws/things/Multipass/shadow/update"
keepAliveTime = 1200
IRCommands = ["Power","Ch+","Ch-","Vol+","Vol-","Mute","Input","1","2","3","4","5","6","7","8","9","0","Enter","Menu","Up","Down","Left","Right","Index","Caption","Audio","Exit"]

# Custom MQTT message callback
def customCallback(client, userdata, message):
        if message.topic==topiccmdPath:
#                print("Received a new command: ")
#                print(message.payload)
#                print("\n")
		lirccmd=""
		for i in IRCommands:
			if str.lower(i) in str.lower(message.payload):
				lirccmd = i
		if lirccmd == "":
			myAWSIoTMQTTClient.publish(topicstatusPath, "Command Not Found", 1)
			print ("command not found")
		else:
			myAWSIoTMQTTClient.publish(topicstatusPath,"lirc command " + lirccmd , 1)
			#Put call to command handler here
			print ("lirc command\n")

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub")
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(topiccmdPath, 1, customCallback)
time.sleep(2)

# Main Loop
loopCount = 0
while True:
	loopCount += 1
	if loopCount >= keepAliveTime:
		loopCount = 0	
		myAWSIoTMQTTClient.publish(topicstatusPath, time.strftime("%I:%M:%S"), 1)
	time.sleep(.1)
