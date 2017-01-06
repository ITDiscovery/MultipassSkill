def lambda_handler(event, context):

    import boto3

    should_end_session = True
    card_title = 'Multipass'
    topiccmdPath = "$aws/things/Multipass/shadow/command"
    topicstatusPath = "$aws/things/Multipass/shadow/update"

    #AlexaCmds = ["Power","Channel","Volume","Mute"]
    #AlexaDirs = ["Up","Down"]
    #IRCmds = ["Power","ChannelUp","ChannelDown","VolumeUp","VolumeDown","Mute"]
    
    #Check Request Type
    SendToShadow = ""
    AlexaResp = ""
    if event['request']['type'] == "IntentRequest":
        #Check and convert Alexa to IRCommands
        KeyStr = event['request']['intent']['slots']['Keys']['value'].decode('utf-8').upper()
        if KeyStr == "CHANNEL":
            try:
                DirStr = event['request']['intent']['slots']['Direction']['value'].decode('utf-8').upper()
            except:
                AlexaResp = "Dort"    
                DirStr = ""
            if DirStr == "UP":
                KeyStr = "CHANNELUP"
            elif DirStr == "DOWN":
                KeyStr = "CHANNELDOWN"
            else:
                AlexaResp = "Dort"
        elif KeyStr == "VOLUME":
            try:
                DirStr = event['request']['intent']['slots']['Direction']['value'].decode('utf-8').upper()
            except:
                AlexaResp = "Dort"
                DirStr = ""
            if DirStr == "UP":
                KeyStr = "VOLUMEUP"
            elif DirStr == "DOWN":
                KeyStr = "VOLUMEDOWN"
            else:
                AlexaResp = "Dort"
        elif KeyStr == "POWER":
            KeyStr = "POWER"
        elif KeyStr == "MUTE":
            KeyStr = "MUTE"
        else:
            # Stanard "Bad" response
            AlexaResp = "Dort"
        # Update the Device Shadow if not bad response
        if AlexaResp != "Dort":
            client = boto3.client('iot-data', region_name='us-east-1')
            #Error Trap this as extra credit
            #response = client.get_thing_shadow(thingName='Multipass')
            SendToShadow = '{"message": "' + SendToShadow + '" }'
            response = client.publish(topic=topiccmdPath,qos=1,payload=SendToShadow)
            AlexaResp = "Ba-da-boom"
    return (build_response({}, build_speechlet_response(card_title, AlexaResp, None, should_end_session)))

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
