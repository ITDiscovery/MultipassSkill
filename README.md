MultipassSkill

Alexa Smart Home Skill that integrates with RPi via MQTT and Shadows

It can be used in conjunction with AlexaPi. 
It born from this case design: http://www.thingiverse.com/thing:1913786

Basic flow is: 
1. Alexa calls Smart Home Skill "Multipass" (Utterance to Intent): 
   "Alexa, tell Multipass Power On"
2. Smart Home Skill "Multipass" converts this to a "Lambda" request:
   "intent":{"name":"Multipass","slots":{"Keys":{"name": "Keys","value":"Power"}}} 
3. The Lambda function takes the request and writes it to a "Shadow" of the 
   thing (written in Python 2.7, (which I didn't find any docs on how to do it):
   $aws/things/Multipass/shadow/command: {"message":"Power"} 
3a. The Lambda function also replies back to the Smart Home Skill with a 
    response: 
    "response":{"outputSpeech":{"type":"PlainText","text":"Baa Dah boom" 
4. Python code running on the Rasberry Pi (MultipassPubSub.py) polls the 
   shawdow (and it can be modified to place what the RPi is doing on that 
   or other shadows).

Installation and implementation instructions will start from back (the RPi)
to the front (Alexa Home Skill).

Steps: 
1. Base install, config network and raspi-config
2. apt-get update and upgrade 
3. sudo apt-get install git pip 
4. sudo pip install paho-mqtt 
5(Opt). Install Alexa-pi if you want via https://github.com/alexa-pi/AlexaPi 
6. sudo git clone https://github.com/itdiscovery/MultipassSkill

