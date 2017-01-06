<B>MultipassSkill</B> ---Warning!! Mostly complete, but not fully vetted.

Alexa Smart Home Skill that integrates with RPi via MQTT and Shadows

It can be used in conjunction with AlexaPi. 
It born from this case design: http://www.thingiverse.com/thing:1913786

Basic flow is: 
<ol><li>Alexa calls Smart Home Skill "Multipass" (Utterance to Intent): "Alexa, tell Multipass Power On"</li>
<li>Smart Home Skill "Multipass" converts this to a "Lambda" request: "intent":{"name":"Multipass","slots":{"Keys":{"name": "Keys","value":"Power"}}} </li>
<li>The Lambda function takes the request, traps invalid commands, and writes it to a "Shadow" of the thing (written in Python 2.7, (which I didn't find any docs on how to do it): $aws/things/Multipass/shadow/command: {"message":"POWER"} </li>
<li>The Lambda function also replies back to the Smart Home Skill with a response: "response":{"outputSpeech {"type":"PlainText","text":"Baa Dah boom"}}</li>
<li>Python code running on the Rasberry Pi (MultipassPubSub.py) polls the shawdow (and it can be modified to place what the RPi is doing on that or other shadows).</li></ol>

Steps for Alexa install:
<ul>



<li>Create (if needed, you'd need it for AlexaPi) an Amazon developer account at https://developer.amazon.com</li>
<li>Navigate to the Alexa Skills page at https://developer.amazon.com/edw/home.html#/skills/list and then add a new skill.</li>
<li>The Skill Information page: Give your skill a name and click "No" on the Audio Player section. I captured the Applicaiton ID for my records. </li>
<li>The Intent Schema page: Complete this page from the data provided in the Interaction_IntentSchema file.</li>
<li>The Configuration page: The Service Endpoint is "AWS Lambda ARN". The geographic region is "North America", and the ARN is from the Lambda fuction from above. Mark "No" for "Account Linking".</li>
<li>The Publishing Information page: I marked my the "Category" as "Smart Home", "Testing Instructions" as "Raspberry Pi IR Handler, Requires MultipassPubSub.py running on RPi, run from command line to view commands as they are passed." 
Countries & Region: is "All countries". Short Skill Description is "Raspberry Pi IR Handler". I used the Thingiverse description for the RPi build in the Full Skill Description. For Example Phrases I used: "Alexa tell Multipass to Power", "Alexa tell Multipass Power", "Alexa ask Multipass Power On". Keywords: "Smart,Home,Raspberry,Pi,Lirc,Implementation". You absolutely have to use</li>

</ul>

Steps for RPi Install: 
<ul><li>Base install, config network and raspi-config</li>
<li>sudo apt-get update and upgrade </li>
<li>sudo apt-get install git pip </li>
<li>sudo pip install paho-mqtt </li>
<li>sudo pip install AWSIoTPythonSDK </li>
<li>(Opt). Install Alexa-pi if you want via https://github.com/alexa-pi/AlexaPi </li>
<li>sudo git clone https://github.com/itdiscovery/MultipassSkill</li>
<li>cp Multipass.service /lib/systemd/system/Multipass.service</li>
<li>sudo chmod 644 /lib/systemd/system/Multipass.service</li>
<li>sudo systemctl daemon-reload</li>
<li>sudo systemctl enable Multipass.service</li>


</ul>
