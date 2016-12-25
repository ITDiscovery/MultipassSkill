'''
/*
 * Modified by Peter Nichols (raspbian@itdiscover.info)
 * December 2016 for connection to Amazon Voice Services. See
 * http://github.com/itdiscovery/MultipassSkill
 *
 * Expects LIRC to be installed
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

import subprocess
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import getopt

# Command Line Parameters
remotenm = "insignia"
host = "Your Thing Shadow's Rest API Endpoint Goes Here"
rootCAPath = "root-CA.crt"
certificatePath = "Multipass.cert.pem"
privateKeyPath = "Multipass.private.key"
topiccmdPath = "$aws/things/Multipass/shadow/command"
topicstatusPath = "$aws/things/Multipass/shadow/update"
keepAliveTime = 1200
IRCommands = ["Power","Ch+","Ch-","Vol+","Vol-","Mute","Input","1","2","3","4",
	"5","6","7","8","9","0"]
LIRCKeys = ["POWER","CHANNELUP","CHANNELDOWN","VOLUMEUP","VOLUMEDOWN","MUTE",
	"ESC","1","2","3","4","5","6","7","8","9","0"]

# Custom MQTT message callback
def customCallback(client, userdata, message):
        if message.topic==topiccmdPath:
		# Received a new command to the shadow (contained in message.payload).
		# Check the list of commands and map it against an action (or however you want
		# structure the action portion of the code.
		for i, lirccmd in enumerate(IRCommands, start=0):
			if str.upper(IRCommands[i]) in str.upper(message.payload):
	                        #The command was found, process it via subroutine in this case a remap
				rtn = subprocess.call(["irsend", "SEND_ONCE", remotenm, "KEY_" + LIRCKeys[i]])
	                        #syscmd = "irsend SEND_ONCE " + remotenm + " KEY_" + LIRCKeys[i]
        	                #retn = subprocess.call([syscmd, i], shell=False)
				#Send the acknowledge the command was successfuly sent
				myAWSIoTMQTTClient.publish(topicstatusPath,"irsend SEND_ONCE " + remotenm + LIRCKeys[i] + "=" + str(rtn) , 1)
				break
		else:
			myAWSIoTMQTTClient.publish(topicstatusPath, "Command Not Found", 1)
			print ("command not found")
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
